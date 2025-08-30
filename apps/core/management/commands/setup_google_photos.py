"""
Django management command to set up Google Photos API credentials and album.
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import json


class Command(BaseCommand):
    help = 'Set up Google Photos API integration for treasure hunt photos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--setup-credentials',
            action='store_true',
            help='Create a template for Google Photos credentials',
        )
        parser.add_argument(
            '--album-url',
            type=str,
            help='Google Photos album URL to extract album ID from',
        )
        parser.add_argument(
            '--credentials-file',
            type=str,
            help='Path to Google Photos API credentials JSON file',
        )

    def handle(self, *args, **options):
        if options['setup_credentials']:
            self.setup_credentials_template()
        
        if options['album_url']:
            self.extract_album_id(options['album_url'])
        
        if options['credentials_file']:
            self.setup_credentials_file(options['credentials_file'])

    def setup_credentials_template(self):
        """Create a template for Google Photos credentials"""
        credentials_path = os.path.join(settings.BASE_DIR, 'google_photos_credentials_template.json')
        
        template = {
            "web": {
                "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
                "project_id": "your-project-id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "YOUR_CLIENT_SECRET",
                "redirect_uris": ["http://localhost:8080/callback"]
            }
        }
        
        with open(credentials_path, 'w') as f:
            json.dump(template, f, indent=2)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Created credentials template at: {credentials_path}\n'
                'Please fill in your Google Cloud Project credentials and rename to "google_photos_credentials.json"'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\nTo set up Google Photos API:\n'
                '1. Go to Google Cloud Console (https://console.cloud.google.com/)\n'
                '2. Create a new project or select existing one\n'
                '3. Enable the Photos Library API\n'
                '4. Create OAuth 2.0 credentials (Web application)\n'
                '5. Add http://localhost:8080/callback to authorized redirect URIs\n'
                '6. Download the credentials JSON file\n'
                '7. Copy the credentials to google_photos_credentials.json\n'
                '8. Run: python manage.py setup_google_photos --album-url "YOUR_ALBUM_URL"'
            )
        )

    def extract_album_id(self, album_url):
        """Extract album ID from Google Photos album URL"""
        # Example URL: https://photos.app.goo.gl/sDnZoj5VnkZ4yByS6
        # We need to handle the shortened URL
        
        self.stdout.write(f'Processing album URL: {album_url}')
        
        # For the shortened URL format, we can't directly extract the album ID
        # The user will need to get the full album ID from the Google Photos API
        
        if 'photos.app.goo.gl' in album_url:
            self.stdout.write(
                self.style.WARNING(
                    'This is a shortened Google Photos URL. To get the album ID:\n'
                    '1. Open the album in your browser\n'
                    '2. Look for the full URL which contains the album ID\n'
                    '3. Or use the Google Photos API to list your albums\n'
                    '4. Set GOOGLE_PHOTOS_ALBUM_ID in your environment variables'
                )
            )
            
            # Create a helper script to get album ID
            helper_script = os.path.join(settings.BASE_DIR, 'get_google_photos_album_id.py')
            script_content = '''
import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

def authenticate():
    """Authenticate with Google Photos API"""
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
    creds = None
    
    # Load existing token
    if os.path.exists('google_photos_token.json'):
        creds = Credentials.from_authorized_user_file('google_photos_token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file('google_photos_credentials.json', SCOPES)
            flow.redirect_uri = 'http://localhost:8080/callback'
            
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f'Please go to this URL: {auth_url}')
            code = input('Enter the authorization code: ')
            flow.fetch_token(code=code)
            creds = flow.credentials
        
        # Save the credentials for the next run
        with open('google_photos_token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('photoslibrary', 'v1', credentials=creds)

def list_albums():
    """List all albums"""
    service = authenticate()
    
    albums = []
    page_token = None
    
    while True:
        response = service.albums().list(pageToken=page_token).execute()
        albums.extend(response.get('albums', []))
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    
    print(f"Found {len(albums)} albums:")
    for album in albums:
        print(f"- {album['title']}: {album['id']}")
        if 'productUrl' in album:
            print(f"  URL: {album['productUrl']}")
        print()

if __name__ == '__main__':
    try:
        list_albums()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have google_photos_credentials.json in this directory")
'''
            
            with open(helper_script, 'w') as f:
                f.write(script_content)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created helper script: {helper_script}\n'
                    'Run this script to list your Google Photos albums and find the correct album ID.'
                )
            )
        
        else:
            # Try to extract from full URL format
            if 'albumid=' in album_url:
                album_id = album_url.split('albumid=')[1].split('&')[0]
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Extracted album ID: {album_id}\n'
                        f'Add this to your environment: GOOGLE_PHOTOS_ALBUM_ID="{album_id}"'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        'Could not extract album ID from URL. Please use the helper script to find it.'
                    )
                )

    def setup_credentials_file(self, credentials_file):
        """Set up credentials file"""
        if not os.path.exists(credentials_file):
            raise CommandError(f'Credentials file not found: {credentials_file}')
        
        target_path = os.path.join(settings.BASE_DIR, 'google_photos_credentials.json')
        
        # Copy the file
        import shutil
        shutil.copy2(credentials_file, target_path)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Copied credentials file to: {target_path}\n'
                'Google Photos integration is now ready!'
            )
        )
