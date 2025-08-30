"""
Production-ready Google Photos service for Render deployment.
Supports both OAuth 2.0 and Service Account authentication.
"""

import os
import json
import logging
import tempfile
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.files.storage import default_storage
import requests

logger = logging.getLogger(__name__)


class RenderGooglePhotosService:
    """
    Production Google Photos service optimized for Render deployment.
    Supports service account authentication for server-to-server operations.
    """
    
    def __init__(self):
        self.album_id = getattr(settings, 'GOOGLE_PHOTOS_ALBUM_ID', None)
        self.album_url = f"https://photos.app.goo.gl/{self.album_id}" if self.album_id else None
        self.service = None
        self.credentials = None
        self.auth_type = self._detect_auth_type()
        
    def _detect_auth_type(self):
        """Detect whether to use service account or OAuth 2.0"""
        service_account_key = os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY')
        service_account_file = getattr(settings, 'GOOGLE_SERVICE_ACCOUNT_FILE', '')
        
        if service_account_key or (service_account_file and os.path.exists(service_account_file)):
            return 'service_account'
        else:
            return 'oauth2'
    
    def is_configured(self):
        """Check if Google Photos is properly configured for production"""
        if not getattr(settings, 'GOOGLE_PHOTOS_ENABLED', False):
            return False
            
        if not self.album_id:
            return False
            
        if self.auth_type == 'service_account':
            return self._has_service_account_credentials()
        else:
            return self._has_oauth_credentials()
    
    def _has_service_account_credentials(self):
        """Check if service account credentials are available"""
        # Check environment variable (preferred for Render)
        if os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY'):
            return True
            
        # Check file (fallback)
        service_account_file = getattr(settings, 'GOOGLE_SERVICE_ACCOUNT_FILE', '')
        return service_account_file and os.path.exists(service_account_file)
    
    def _has_oauth_credentials(self):
        """Check if OAuth credentials are available"""
        creds_file = getattr(settings, 'GOOGLE_PHOTOS_CREDENTIALS_FILE', '')
        return creds_file and os.path.exists(creds_file)
    
    def authenticate(self):
        """Authenticate with Google Photos API"""
        if self.service:
            return True
            
        try:
            if self.auth_type == 'service_account':
                return self._authenticate_service_account()
            else:
                return self._authenticate_oauth()
                
        except ImportError:
            logger.error("Google Photos API libraries not installed")
            return False
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Photos: {e}")
            return False
    
    def _authenticate_service_account(self):
        """Authenticate using service account (preferred for production)"""
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/photoslibrary']
            
            # Try environment variable first (Render deployment)
            service_account_key = os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY')
            if service_account_key:
                # Parse JSON from environment variable
                service_account_info = json.loads(service_account_key)
                credentials = service_account.Credentials.from_service_account_info(
                    service_account_info, scopes=SCOPES
                )
                logger.info("Using service account from environment variable")
            else:
                # Fallback to file
                service_account_file = getattr(settings, 'GOOGLE_SERVICE_ACCOUNT_FILE', '')
                if not os.path.exists(service_account_file):
                    logger.error("Service account file not found")
                    return False
                    
                credentials = service_account.Credentials.from_service_account_file(
                    service_account_file, scopes=SCOPES
                )
                logger.info("Using service account from file")
            
            self.credentials = credentials
            self.service = build('photoslibrary', 'v1', credentials=credentials)
            return True
            
        except Exception as e:
            logger.error(f"Service account authentication failed: {e}")
            return False
    
    def _authenticate_oauth(self):
        """Authenticate using OAuth 2.0 (for development)"""
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/photoslibrary']
            
            creds_file = getattr(settings, 'GOOGLE_PHOTOS_CREDENTIALS_FILE', '')
            token_file = getattr(settings, 'GOOGLE_PHOTOS_TOKEN_FILE', '')
            
            creds = None
            
            # Load existing token
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            
            # If there are no valid credentials, get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(creds_file):
                        logger.error("OAuth credentials file not found")
                        return False
                    
                    # This won't work in production without user interaction
                    logger.warning("OAuth flow requires user interaction - not suitable for production")
                    return False
                
                # Save credentials for next run
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            self.credentials = creds
            self.service = build('photoslibrary', 'v1', credentials=creds)
            return True
            
        except Exception as e:
            logger.error(f"OAuth authentication failed: {e}")
            return False
    
    def upload_photo(self, photo_file, description: str = "", player_name: str = "", question_order: int = None) -> Optional[Dict[str, Any]]:
        """Upload a photo to Google Photos"""
        
        if not self.is_configured():
            logger.warning("Google Photos not configured, using fallback")
            return self._fallback_response(photo_file, description, player_name, question_order)
        
        try:
            return self._real_upload(photo_file, description, player_name, question_order)
        except Exception as e:
            logger.error(f"Google Photos upload failed: {e}")
            return self._fallback_response(photo_file, description, player_name, question_order)
    
    def _real_upload(self, photo_file, description: str, player_name: str, question_order: int) -> Optional[Dict[str, Any]]:
        """Perform real upload to Google Photos"""
        if not self.authenticate():
            raise Exception("Authentication failed")
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            if hasattr(photo_file, 'read'):
                photo_file.seek(0)
                for chunk in photo_file.chunks():
                    temp_file.write(chunk)
            else:
                temp_file.write(photo_file)
            temp_path = temp_file.name
        
        try:
            # Upload the photo
            upload_token = self._upload_bytes(temp_path)
            if not upload_token:
                raise Exception("Failed to get upload token")
            
            # Create media item
            media_item = self._create_media_item(
                upload_token, 
                description, 
                player_name, 
                question_order
            )
            
            if not media_item:
                raise Exception("Failed to create media item")
            
            # Add to album if configured
            if self.album_id:
                self._add_to_album(media_item['id'])
            
            logger.info(f"Successfully uploaded photo to Google Photos for {player_name}")
            
            return {
                'media_item_id': media_item['id'],
                'base_url': media_item.get('baseUrl'),
                'product_url': media_item.get('productUrl'),
                'filename': media_item.get('filename'),
                'mime_type': media_item.get('mimeType'),
                'album_url': self.album_url,
                'auth_type': self.auth_type
            }
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _fallback_response(self, photo_file, description: str, player_name: str, question_order: int) -> Dict[str, Any]:
        """Generate fallback response when real upload isn't available"""
        original_name = getattr(photo_file, 'name', f'photo_{player_name}_{question_order}.jpg')
        base_filename = os.path.splitext(original_name)[0]
        simulated_media_id = f"fallback_{hash(f'{player_name}_{question_order}_{base_filename}')}"
        
        logger.info(f"Using fallback for {player_name}, question {question_order}")
        
        return {
            'media_item_id': simulated_media_id,
            'base_url': f"https://via.placeholder.com/400x300/lightblue/darkblue?text=Uploaded+Photo",
            'product_url': self.album_url,
            'filename': original_name,
            'mime_type': 'image/jpeg',
            'album_url': self.album_url,
            'fallback': True,
            'auth_type': self.auth_type
        }
    
    def _upload_bytes(self, file_path: str) -> Optional[str]:
        """Upload photo bytes and get upload token"""
        try:
            with open(file_path, 'rb') as f:
                photo_bytes = f.read()
            
            upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
            headers = {
                'Authorization': f'Bearer {self.credentials.token}',
                'Content-Type': 'application/octet-stream',
                'X-Goog-Upload-File-Name': os.path.basename(file_path),
                'X-Goog-Upload-Protocol': 'raw'
            }
            
            response = requests.post(upload_url, data=photo_bytes, headers=headers)
            
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"Failed to upload bytes: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error uploading bytes: {e}")
            return None
    
    def _create_media_item(self, upload_token: str, description: str, player_name: str, question_order: int) -> Optional[Dict[str, Any]]:
        """Create media item from upload token"""
        try:
            filename = f"onam_treasure_hunt_q{question_order}_{player_name}.jpg" if question_order else f"onam_photo_{player_name}.jpg"
            
            request_body = {
                'newMediaItems': [
                    {
                        'description': f"{description}\nPlayer: {player_name}\nQuestion: {question_order}" if question_order else f"{description}\nPlayer: {player_name}",
                        'simpleMediaItem': {
                            'fileName': filename,
                            'uploadToken': upload_token
                        }
                    }
                ]
            }
            
            if self.album_id:
                request_body['albumId'] = self.album_id
            
            response = self.service.mediaItems().batchCreate(body=request_body).execute()
            
            new_media_items = response.get('newMediaItemResults', [])
            if new_media_items and 'mediaItem' in new_media_items[0]:
                return new_media_items[0]['mediaItem']
            else:
                logger.error(f"Failed to create media item: {response}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating media item: {e}")
            return None
    
    def _add_to_album(self, media_item_id: str) -> bool:
        """Add media item to album"""
        if not self.album_id:
            return False
        
        try:
            request_body = {
                'mediaItemIds': [media_item_id]
            }
            
            self.service.albums().batchAddMediaItems(
                albumId=self.album_id,
                body=request_body
            ).execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to add media item to album: {e}")
            return False


# Use the production-ready service
google_photos_service = RenderGooglePhotosService()
GOOGLE_PHOTOS_AVAILABLE = True

# Export for backward compatibility
__all__ = ['google_photos_service', 'GOOGLE_PHOTOS_AVAILABLE', 'RenderGooglePhotosService']
