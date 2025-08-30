"""
Django management command to debug and fix media file issues
for treasure hunt images and photos.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from apps.core.models import TreasureHuntQuestion, PlayerAnswer
import os
import requests


class Command(BaseCommand):
    help = 'Debug and fix media file issues for treasure hunt'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-images',
            action='store_true',
            help='Check if question images are accessible',
        )
        parser.add_argument(
            '--check-photos',
            action='store_true',
            help='Check if uploaded photos are accessible',
        )
        parser.add_argument(
            '--fix-permissions',
            action='store_true',
            help='Fix file permissions for media files',
        )
        parser.add_argument(
            '--show-urls',
            action='store_true',
            help='Show all media URLs for debugging',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔍 Debugging treasure hunt media files...')
        )

        if options['check_images']:
            self.check_question_images()
        
        if options['check_photos']:
            self.check_uploaded_photos()
        
        if options['fix_permissions']:
            self.fix_file_permissions()
        
        if options['show_urls']:
            self.show_media_urls()
        
        if not any([options['check_images'], options['check_photos'], 
                   options['fix_permissions'], options['show_urls']]):
            # Run all checks by default
            self.check_question_images()
            self.check_uploaded_photos()
            self.show_media_urls()

    def check_question_images(self):
        """Check if question images are accessible"""
        self.stdout.write('\n📸 Checking question images...')
        
        questions_with_images = TreasureHuntQuestion.objects.filter(
            question_image__isnull=False
        ).exclude(question_image='')
        
        if not questions_with_images.exists():
            self.stdout.write('📍 No question images found')
            return
        
        for question in questions_with_images:
            image_path = question.question_image.name
            image_url = question.question_image.url
            
            self.stdout.write(f'\n🔍 Question {question.order}:')
            self.stdout.write(f'   File: {image_path}')
            self.stdout.write(f'   URL: {image_url}')
            
            # Check if file exists
            if default_storage.exists(image_path):
                file_size = default_storage.size(image_path)
                self.stdout.write(
                    self.style.SUCCESS(f'   ✅ File exists ({file_size} bytes)')
                )
                
                # Check if URL is accessible
                try:
                    full_url = f"{settings.MEDIA_URL.rstrip('/')}{image_url}"
                    self.stdout.write(f'   Testing URL: {full_url}')
                    
                    # For local testing, check file system
                    if hasattr(settings, 'MEDIA_ROOT'):
                        full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                        if os.path.exists(full_path):
                            self.stdout.write(
                                self.style.SUCCESS('   ✅ File accessible on filesystem')
                            )
                        else:
                            self.stdout.write(
                                self.style.ERROR('   ❌ File not found on filesystem')
                            )
                
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'   ❌ URL check failed: {e}')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR('   ❌ File not found in storage')
                )

    def check_uploaded_photos(self):
        """Check uploaded treasure hunt photos"""
        self.stdout.write('\n📱 Checking uploaded photos...')
        
        photo_answers = PlayerAnswer.objects.filter(
            photo_answer__isnull=False
        ).exclude(photo_answer='')
        
        if not photo_answers.exists():
            self.stdout.write('📍 No uploaded photos found')
            return
        
        for answer in photo_answers[:10]:  # Check first 10
            photo_path = answer.photo_answer.name
            photo_url = answer.photo_answer.url
            
            self.stdout.write(f'\n🔍 {answer.player.name} - Q{answer.question.order}:')
            self.stdout.write(f'   File: {photo_path}')
            self.stdout.write(f'   URL: {photo_url}')
            
            if answer.google_photos_url:
                self.stdout.write(f'   Google Photos: {answer.google_photos_url}')
            
            # Check if file exists
            if default_storage.exists(photo_path):
                file_size = default_storage.size(photo_path)
                self.stdout.write(
                    self.style.SUCCESS(f'   ✅ File exists ({file_size} bytes)')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('   ❌ File not found in storage')
                )

    def fix_file_permissions(self):
        """Fix file permissions for media files"""
        self.stdout.write('\n🔧 Fixing file permissions...')
        
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if not media_root:
            self.stdout.write(
                self.style.ERROR('❌ MEDIA_ROOT not configured')
            )
            return
        
        try:
            # Make sure media directory exists
            os.makedirs(media_root, exist_ok=True)
            
            # Set proper permissions
            for root, dirs, files in os.walk(media_root):
                # Set directory permissions
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    os.chmod(dir_path, 0o755)
                
                # Set file permissions
                for f in files:
                    file_path = os.path.join(root, f)
                    os.chmod(file_path, 0o644)
            
            self.stdout.write(
                self.style.SUCCESS('✅ File permissions fixed')
            )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to fix permissions: {e}')
            )

    def show_media_urls(self):
        """Show media URL configuration for debugging"""
        self.stdout.write('\n🌐 Media URL Configuration:')
        
        self.stdout.write(f'📍 MEDIA_URL: {settings.MEDIA_URL}')
        self.stdout.write(f'📍 MEDIA_ROOT: {getattr(settings, "MEDIA_ROOT", "Not set")}')
        self.stdout.write(f'📍 DEBUG: {settings.DEBUG}')
        
        # Check some sample URLs
        questions_with_images = TreasureHuntQuestion.objects.filter(
            question_image__isnull=False
        ).exclude(question_image='')[:3]
        
        if questions_with_images.exists():
            self.stdout.write('\n🔗 Sample question image URLs:')
            for question in questions_with_images:
                self.stdout.write(f'   Q{question.order}: {question.question_image.url}')
        
        photo_answers = PlayerAnswer.objects.filter(
            photo_answer__isnull=False
        ).exclude(photo_answer='')[:3]
        
        if photo_answers.exists():
            self.stdout.write('\n📱 Sample uploaded photo URLs:')
            for answer in photo_answers:
                self.stdout.write(f'   {answer.player.name}: {answer.photo_answer.url}')
                if answer.google_photos_url:
                    self.stdout.write(f'      Google Photos: {answer.google_photos_url}')
        
        self.stdout.write('\n💡 Troubleshooting tips:')
        self.stdout.write('1. Ensure MEDIA_URL is configured in Django settings')
        self.stdout.write('2. Check that media files are served in production')
        self.stdout.write('3. Verify file upload permissions')
        self.stdout.write('4. For Render: Use cloud storage for persistent media files')
        self.stdout.write('5. For Google Photos: Set up API credentials for backup')
