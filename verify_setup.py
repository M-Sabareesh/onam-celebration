#!/usr/bin/env python3
"""Comprehensive test for Onam app setup"""

import os
import sys

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')

try:
    import django
    django.setup()
    print('✅ Django setup successful')
    
    from django.conf import settings
    print(f'✅ Media URL: {settings.MEDIA_URL}')
    print(f'✅ Media Root: {settings.MEDIA_ROOT}')
    print(f'✅ Debug Mode: {settings.DEBUG}')
    
    # Test Google Photos integration
    from apps.core.google_photos import google_photos_service, GOOGLE_PHOTOS_AVAILABLE
    print(f'✅ Google Photos service: {type(google_photos_service).__name__}')
    print(f'✅ Google Photos available: {GOOGLE_PHOTOS_AVAILABLE}')
    
    # Check if Google Photos is configured
    google_enabled = getattr(settings, 'GOOGLE_PHOTOS_ENABLED', False)
    print(f'✅ Google Photos enabled: {google_enabled}')
    
    # Test media files
    media_path = os.path.join(settings.MEDIA_ROOT, 'question_images')
    if os.path.exists(media_path):
        files = os.listdir(media_path)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f'✅ Question images found: {len(image_files)}')
        for img in image_files:
            print(f'   📄 {img}')
    else:
        print('❌ Question images directory not found')
    
    print('\n🎉 Basic setup verification complete!')
    print('\n🚀 To start server: python manage.py runserver')
    print('🔗 Test image URL: http://localhost:8000/media/question_images/Onma5.jpg')
    
except Exception as e:
    print(f'❌ Error during setup: {e}')
    import traceback
    traceback.print_exc()
