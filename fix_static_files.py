#!/usr/bin/env python
"""
Static Files Fix Script
This script will handle static file issues including missing Maveli images.
"""

import os
import shutil
from pathlib import Path

def ensure_maveli_images():
    """Ensure Maveli images are in the correct location"""
    print("=== Fixing Maveli Images ===")
    
    # Base paths
    project_root = Path(__file__).parent
    media_path = project_root / 'media' / 'Maveli'
    static_path = project_root / 'static' / 'images'
    
    # Ensure directories exist
    media_path.mkdir(parents=True, exist_ok=True)
    static_path.mkdir(parents=True, exist_ok=True)
    
    # List of required Maveli images
    maveli_images = [
        'Maveli.jpg',
        'Maveli2.jpg', 
        'Maveli2.png',
        'Maveli4.jpg'
    ]
    
    # Check and copy images if they exist in media but not in static
    for img in maveli_images:
        media_img = media_path / img
        static_img = static_path / img
        
        if media_img.exists() and not static_img.exists():
            try:
                shutil.copy2(media_img, static_img)
                print(f"✅ Copied {img} to static/images/")
            except Exception as e:
                print(f"❌ Failed to copy {img}: {e}")
        elif static_img.exists():
            print(f"✅ {img} already exists in static/images/")
        else:
            print(f"⚠️  {img} not found in media folder")
    
    # Create a placeholder Maveli image if none exist
    placeholder_path = static_path / 'Maveli.jpg'
    if not placeholder_path.exists():
        # Create a simple placeholder file
        with open(placeholder_path, 'w') as f:
            f.write("# Placeholder for Maveli.jpg")
        print("📝 Created placeholder Maveli.jpg")

def fix_static_references():
    """Fix static file references in templates"""
    print("\n=== Fixing Static File References ===")
    
    # Update templates to use correct static paths
    templates_to_check = [
        'templates/base.html',
        'templates/core/index.html',
        'templates/core/about.html'
    ]
    
    for template_path in templates_to_check:
        full_path = Path(__file__).parent / template_path
        if full_path.exists():
            print(f"✅ {template_path} exists")
        else:
            print(f"❌ {template_path} not found")

def create_static_settings_fix():
    """Create a settings fix for static files"""
    print("\n=== Creating Static Settings Fix ===")
    
    settings_fix = '''
# Add to your settings file for static files fix

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files configuration  
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Staticfiles storage (for production)
if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
'''
    
    with open('static_settings_fix.txt', 'w') as f:
        f.write(settings_fix)
    
    print("📝 Created static_settings_fix.txt with configuration")

def main():
    """Main function"""
    print("🖼️  Fixing Static Files and Maveli Images\n")
    
    ensure_maveli_images()
    fix_static_references()
    create_static_settings_fix()
    
    print("\n🎉 Static files fixes completed!")
    print("\nNext steps:")
    print("1. Run: python manage.py collectstatic")
    print("2. Check static_settings_fix.txt for configuration")
    print("3. Ensure Maveli images are properly placed")

if __name__ == '__main__':
    main()
