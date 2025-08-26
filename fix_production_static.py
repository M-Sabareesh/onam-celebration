#!/usr/bin/env python
"""
Production Static Files Fix for Maveli Images
This script fixes the missing Maveli images issue on Render deployment.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from pathlib import Path

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
    django.setup()

def fix_maveli_images():
    """Fix missing Maveli images in static files"""
    print("🖼️  Fixing Maveli images for production...")
    
    # Get paths
    static_root = Path(settings.STATIC_ROOT) if hasattr(settings, 'STATIC_ROOT') else Path('staticfiles')
    static_images_dir = static_root / 'images'
    
    # Ensure images directory exists
    static_images_dir.mkdir(parents=True, exist_ok=True)
    
    # List of Maveli images that need to exist
    maveli_images = [
        'Maveli.jpg',
        'Maveli2.jpg', 
        'Maveli2.png',
        'Maveli4.jpg'
    ]
    
    # Create placeholder images if they don't exist
    for img_name in maveli_images:
        img_path = static_images_dir / img_name
        if not img_path.exists():
            # Create a minimal placeholder file
            with open(img_path, 'wb') as f:
                # Write minimal JPEG header for .jpg files or PNG header for .png files
                if img_name.endswith('.jpg'):
                    # Minimal JPEG header
                    f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')
                else:  # PNG
                    # Minimal PNG header
                    f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x04\x00\x01]\xcc[\x1a\x00\x00\x00\x00IEND\xaeB`\x82')
            
            print(f"📝 Created placeholder {img_name}")
        else:
            print(f"✅ {img_name} already exists")

def update_templates_to_use_safe_static():
    """Update templates to handle missing static files gracefully"""
    print("\n🔧 Creating template fix for safe static file loading...")
    
    template_fix = '''
<!-- Add this to your base template to handle missing Maveli images gracefully -->
{% load static %}

<!-- Safe Maveli image loading -->
<script>
function handleMaveliImageError(img) {
    // If Maveli image fails to load, hide it or use a fallback
    img.style.display = 'none';
    console.log('Maveli image not found:', img.src);
}
</script>

<!-- Use this pattern for Maveli images -->
<!-- 
<img src="{% static 'images/Maveli.jpg' %}" 
     alt="Maveli" 
     onerror="handleMaveliImageError(this)"
     style="max-height: 60px;">
-->
'''
    
    with open('template_static_fix.html', 'w') as f:
        f.write(template_fix)
    
    print("📝 Created template_static_fix.html with safe image loading")

def create_static_files_settings():
    """Create production-safe static files settings"""
    print("\n⚙️  Creating production static files configuration...")
    
    settings_content = '''
# Production Static Files Settings for Render

import os
from pathlib import Path

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Use whitenoise for static files serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Whitenoise settings for better static file handling
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Alternative: Use regular storage if manifest storage causes issues
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
'''
    
    with open('production_static_settings.py', 'w') as f:
        f.write(settings_content)
    
    print("📝 Created production_static_settings.py")

def run_collectstatic():
    """Run collectstatic to regenerate manifest"""
    print("\n🔄 Running collectstatic to regenerate manifest...")
    
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
        print("✅ Static files collected successfully")
        return True
    except Exception as e:
        print(f"⚠️  Collectstatic had issues: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Production Static Files Fix for Maveli Images")
    print("=" * 50)
    
    # Setup Django
    setup_django()
    
    # Fix Maveli images
    fix_maveli_images()
    
    # Create template fix
    update_templates_to_use_safe_static()
    
    # Create settings configuration
    create_static_files_settings()
    
    # Regenerate static files
    if run_collectstatic():
        print("\n🎉 Static files fix completed!")
        print("\nNext steps:")
        print("1. Restart your Render service")
        print("2. Check that Maveli images load properly")
        print("3. If issues persist, check production_static_settings.py")
    else:
        print("\n⚠️  Static files collection had issues")
        print("You may need to manually fix the static files configuration")

if __name__ == '__main__':
    main()
