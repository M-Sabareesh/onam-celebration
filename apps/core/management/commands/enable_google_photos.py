"""
Management command to enable and test Google Photos integration.
"""

import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.core.google_photos import google_photos_service, GOOGLE_PHOTOS_AVAILABLE


class Command(BaseCommand):
    help = 'Enable and test Google Photos integration for treasure hunt photos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--setup',
            action='store_true',
            help='Set up Google Photos credentials interactively',
        )
        parser.add_argument(
            '--test',
            action='store_true',
            help='Test Google Photos upload with a sample image',
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='Check Google Photos integration status',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('🔗 Google Photos Integration Manager'))
        self.stdout.write('=' * 50)

        if options['status'] or not any([options['setup'], options['test']]):
            self.check_status()

        if options['setup']:
            self.setup_credentials()

        if options['test']:
            self.test_upload()

    def check_status(self):
        """Check the current status of Google Photos integration"""
        self.stdout.write('\n📊 Current Status:')
        
        # Check if enabled in settings
        enabled = getattr(settings, 'GOOGLE_PHOTOS_ENABLED', False)
        self.stdout.write(f'  • Enabled in settings: {self.yes_no(enabled)}')
        
        # Check for credentials file
        creds_file = getattr(settings, 'GOOGLE_PHOTOS_CREDENTIALS_FILE', '')
        creds_exists = os.path.exists(creds_file) if creds_file else False
        self.stdout.write(f'  • Credentials file: {self.yes_no(creds_exists)}')
        if creds_exists:
            self.stdout.write(f'    📁 Path: {creds_file}')
        
        # Check for token file
        token_file = getattr(settings, 'GOOGLE_PHOTOS_TOKEN_FILE', '')
        token_exists = os.path.exists(token_file) if token_file else False
        self.stdout.write(f'  • Token file: {self.yes_no(token_exists)}')
        
        # Check album ID
        album_id = getattr(settings, 'GOOGLE_PHOTOS_ALBUM_ID', '')
        self.stdout.write(f'  • Album ID: {album_id if album_id else "Not set"}')
        
        # Check if libraries are available
        self.stdout.write(f'  • Google libraries available: {self.yes_no(GOOGLE_PHOTOS_AVAILABLE)}')
        
        # Overall status
        overall_ready = enabled and creds_exists and GOOGLE_PHOTOS_AVAILABLE
        status_color = self.style.SUCCESS if overall_ready else self.style.WARNING
        self.stdout.write(f'\n🎯 Overall Status: {status_color("READY" if overall_ready else "NEEDS SETUP")}')
        
        if not overall_ready:
            self.stdout.write('\n💡 To enable Google Photos integration:')
            if not enabled:
                self.stdout.write('  1. Set GOOGLE_PHOTOS_ENABLED=True in your environment')
            if not creds_exists:
                self.stdout.write('  2. Run: python manage.py enable_google_photos --setup')
            if not GOOGLE_PHOTOS_AVAILABLE:
                self.stdout.write('  3. Install Google API libraries: pip install -r requirements.txt')

    def setup_credentials(self):
        """Interactive setup for Google Photos credentials"""
        self.stdout.write('\n🔧 Setting up Google Photos credentials...')
        
        self.stdout.write('\n📝 Steps to get Google Photos API credentials:')
        self.stdout.write('1. Go to: https://console.cloud.google.com/')
        self.stdout.write('2. Create a new project or select existing one')
        self.stdout.write('3. Enable the "Photos Library API"')
        self.stdout.write('4. Create credentials (OAuth 2.0 Client ID)')
        self.stdout.write('5. Download the JSON file')
        
        # Get credentials file path
        default_path = getattr(settings, 'GOOGLE_PHOTOS_CREDENTIALS_FILE', 
                              os.path.join(settings.BASE_DIR, 'google_photos_credentials.json'))
        
        creds_path = input(f'\nEnter path to credentials JSON file [{default_path}]: ').strip()
        if not creds_path:
            creds_path = default_path
        
        if not os.path.exists(creds_path):
            self.stdout.write(self.style.ERROR(f'❌ File not found: {creds_path}'))
            self.stdout.write('Please download the credentials file from Google Cloud Console')
            return
        
        # Validate JSON
        try:
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
                
            if 'installed' not in creds_data and 'web' not in creds_data:
                raise ValueError('Invalid credentials format')
                
            self.stdout.write(self.style.SUCCESS(f'✅ Valid credentials file found'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Invalid credentials file: {e}'))
            return
        
        # Get album ID
        current_album = getattr(settings, 'GOOGLE_PHOTOS_ALBUM_ID', '')
        album_id = input(f'\nEnter Google Photos Album ID [{current_album}]: ').strip()
        if not album_id:
            album_id = current_album
        
        # Update environment variables suggestion
        self.stdout.write(f'\n🔧 Add these to your environment variables:')
        self.stdout.write(f'GOOGLE_PHOTOS_ENABLED=True')
        self.stdout.write(f'GOOGLE_PHOTOS_CREDENTIALS_FILE={creds_path}')
        if album_id:
            self.stdout.write(f'GOOGLE_PHOTOS_ALBUM_ID={album_id}')
        
        self.stdout.write(f'\n✅ Setup complete! Restart the server to apply changes.')

    def test_upload(self):
        """Test Google Photos upload with a sample image"""
        self.stdout.write('\n🧪 Testing Google Photos upload...')
        
        if not GOOGLE_PHOTOS_AVAILABLE:
            self.stdout.write(self.style.ERROR('❌ Google Photos libraries not available'))
            return
        
        if not getattr(settings, 'GOOGLE_PHOTOS_ENABLED', False):
            self.stdout.write(self.style.ERROR('❌ Google Photos not enabled in settings'))
            return
        
        # Check for existing images in media folder
        test_image_path = None
        media_photos = os.path.join(settings.MEDIA_ROOT, 'treasure_hunt_photos')
        
        if os.path.exists(media_photos):
            for filename in os.listdir(media_photos):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    test_image_path = os.path.join(media_photos, filename)
                    break
        
        if not test_image_path:
            self.stdout.write(self.style.WARNING('⚠️  No test images found in media/treasure_hunt_photos/'))
            return
        
        # Try to upload
        try:
            with open(test_image_path, 'rb') as f:
                test_file = SimpleUploadedFile(
                    name=os.path.basename(test_image_path),
                    content=f.read(),
                    content_type='image/jpeg'
                )
            
            result = google_photos_service.upload_photo(
                photo_file=test_file,
                description="Test upload from Onam app",
                player_name="Test Player",
                question_order=0
            )
            
            if result:
                self.stdout.write(self.style.SUCCESS('✅ Test upload successful!'))
                self.stdout.write(f'  📸 Media ID: {result.get("media_item_id", "N/A")}')
                self.stdout.write(f'  🔗 URL: {result.get("base_url", "N/A")}')
            else:
                self.stdout.write(self.style.ERROR('❌ Test upload failed'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Upload test failed: {e}'))

    def yes_no(self, value):
        """Format boolean as colored yes/no"""
        if value:
            return self.style.SUCCESS('✅ Yes')
        else:
            return self.style.WARNING('❌ No')
