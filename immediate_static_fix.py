#!/usr/bin/env python3
"""
Immediate Static Files Fix for Production
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

try:
    import django
    django.setup()
    
    print("🔧 IMMEDIATE STATIC FILES FIX")
    print("=" * 35)
    
    # Collect static files
    from django.core.management import call_command
    print("📦 Collecting static files...")
    call_command('collectstatic', verbosity=1, interactive=False, clear=True)
    print("✅ Static files collected")
    
    # Check if Maveli images exist
    from django.conf import settings
    import os
    
    static_images_dir = os.path.join(settings.STATICFILES_DIRS[0], 'images')
    maveli_files = ['Maveli.jpg', 'Maveli2.jpg', 'Maveli4.jpg']
    
    print("🖼️ Checking Maveli images...")
    for image in maveli_files:
        image_path = os.path.join(static_images_dir, image)
        if os.path.exists(image_path):
            print(f"   ✅ {image} found")
        else:
            print(f"   ❌ {image} missing")
    
    print("\n✅ STATIC FILES FIX COMPLETE!")
    print("🔄 Restart your server to see changes")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
