"""
Google Photos API integration for Onam Celebration app.
This service handles uploading treasure hunt photos to a specified Google Photos album.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests

logger = logging.getLogger(__name__)


class GooglePhotosService:
    """Service for interacting with Google Photos API"""
    
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary']
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self.album_id = getattr(settings, 'GOOGLE_PHOTOS_ALBUM_ID', None)
        
    def authenticate(self):
        """Authenticate with Google Photos API"""
        try:
            # Try to load existing credentials
            creds_path = os.path.join(settings.BASE_DIR, 'google_photos_credentials.json')
            token_path = os.path.join(settings.BASE_DIR, 'google_photos_token.json')
            
            creds = None
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
            
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(creds_path):
                        logger.error("Google Photos credentials file not found")
                        return False
                    
                    flow = Flow.from_client_secrets_file(creds_path, self.SCOPES)
                    flow.redirect_uri = 'http://localhost:8080/callback'
                    
                    # This would need to be handled in a web flow for production
                    logger.warning("Google Photos authentication required")
                    return False
                
                # Save the credentials for the next run
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            
            self.credentials = creds
            self.service = build('photoslibrary', 'v1', credentials=creds)
            return True
            
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Photos: {e}")
            return False
    
    def create_album(self, album_title: str) -> Optional[str]:
        """Create a new album in Google Photos"""
        if not self.service:
            if not self.authenticate():
                return None
        
        try:
            request_body = {
                'album': {
                    'title': album_title
                }
            }
            
            response = self.service.albums().create(body=request_body).execute()
            album_id = response.get('id')
            
            logger.info(f"Created Google Photos album: {album_title} (ID: {album_id})")
            return album_id
            
        except Exception as e:
            logger.error(f"Failed to create Google Photos album: {e}")
            return None
    
    def upload_photo(self, photo_file, description: str = "", player_name: str = "", question_order: int = None) -> Optional[Dict[str, Any]]:
        """
        Upload a photo to Google Photos and add it to the specified album
        
        Args:
            photo_file: Django File object or file path
            description: Description for the photo
            player_name: Name of the player uploading
            question_order: Question order number
            
        Returns:
            Dict with photo info including Google Photos URL and media item ID
        """
        if not self.service:
            if not self.authenticate():
                return None
        
        try:
            # Handle Django File object
            if hasattr(photo_file, 'read'):
                # Save the file temporarily if it's a Django File object
                temp_path = default_storage.save(f'temp_upload_{photo_file.name}', photo_file)
                full_temp_path = default_storage.path(temp_path)
            else:
                full_temp_path = photo_file
            
            # Upload the photo
            upload_token = self._upload_bytes(full_temp_path)
            if not upload_token:
                return None
            
            # Create media item
            media_item = self._create_media_item(
                upload_token, 
                description, 
                player_name, 
                question_order
            )
            
            if media_item:
                # Add to album if album_id is configured
                if self.album_id:
                    self._add_to_album(media_item['id'])
                
                # Clean up temp file
                if hasattr(photo_file, 'read'):
                    default_storage.delete(temp_path)
                
                return {
                    'media_item_id': media_item['id'],
                    'base_url': media_item.get('baseUrl'),
                    'product_url': media_item.get('productUrl'),
                    'filename': media_item.get('filename'),
                    'mime_type': media_item.get('mimeType')
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to upload photo to Google Photos: {e}")
            return None
    
    def _upload_bytes(self, file_path: str) -> Optional[str]:
        """Upload photo bytes and get upload token"""
        try:
            # Read the file
            with open(file_path, 'rb') as f:
                photo_bytes = f.read()
            
            # Upload to Google Photos
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
            
            # Add to album if specified
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
    
    def get_album_photos(self) -> list:
        """Get all photos from the configured album"""
        if not self.service or not self.album_id:
            if not self.authenticate():
                return []
        
        try:
            request = self.service.mediaItems().search(
                body={'albumId': self.album_id}
            )
            
            photos = []
            while request is not None:
                response = request.execute()
                photos.extend(response.get('mediaItems', []))
                request = self.service.mediaItems().search_next(request, response)
            
            return photos
            
        except Exception as e:
            logger.error(f"Failed to get album photos: {e}")
            return []
    
    def get_photo_url(self, media_item_id: str, width: int = 800, height: int = 600) -> Optional[str]:
        """Get a resized photo URL from Google Photos"""
        if not self.service:
            if not self.authenticate():
                return None
        
        try:
            media_item = self.service.mediaItems().get(mediaItemId=media_item_id).execute()
            base_url = media_item.get('baseUrl')
            
            if base_url:
                # Add size parameters for better mobile performance
                return f"{base_url}=w{width}-h{height}"
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get photo URL: {e}")
            return None


# Global service instance
google_photos_service = GooglePhotosService()
