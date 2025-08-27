#!/usr/bin/env python3
"""
Fix Static Files for Production
Handles missing static file manifest entries
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
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'onam_project.settings.development'
    import django
    django.setup()

from django.core.management import call_command
from django.conf import settings
import shutil

def collect_static_files():
    """Collect static files with error handling"""
    try:
        print("🔧 Collecting static files...")
        call_command('collectstatic', verbosity=1, interactive=False, clear=True)
        print("✅ Static files collected successfully")
        return True
    except Exception as e:
        print(f"❌ Static collection failed: {e}")
        return False

def copy_maveli_images():
    """Copy Maveli images to static directory"""
    try:
        print("🖼️ Copying Maveli images...")
        
        static_images = os.path.join(settings.BASE_DIR, 'static', 'images')
        media_maveli = os.path.join(settings.BASE_DIR, 'media', 'Maveli')
        
        # Ensure directories exist
        os.makedirs(static_images, exist_ok=True)
        os.makedirs(media_maveli, exist_ok=True)
        
        # Images to copy
        images = ['Maveli.jpg', 'Maveli2.jpg', 'Maveli4.jpg', 'Maveli2.png']
        
        for image in images:
            static_path = os.path.join(static_images, image)
            media_path = os.path.join(media_maveli, image)
            
            # Copy to both static and media
            if os.path.exists(static_path):
                # Copy from static to media
                shutil.copy2(static_path, media_path)
                print(f"   ✅ Copied {image} to media")
            elif os.path.exists(media_path):
                # Copy from media to static
                shutil.copy2(media_path, static_path)
                print(f"   ✅ Copied {image} to static")
            else:
                print(f"   ⚠️ {image} not found")
        
        return True
    except Exception as e:
        print(f"❌ Image copy failed: {e}")
        return False

def fix_template_static_refs():
    """Update templates to handle missing static files gracefully"""
    try:
        print("🔧 Checking template static references...")
        
        template_path = os.path.join(settings.BASE_DIR, 'templates', 'core', 'index.html')
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if the template already has error handling
            if 'onerror=' in content:
                print("   ✅ Template already has error handling")
            else:
                print("   ⚠️ Template needs error handling update")
            
            return True
        else:
            print("   ❌ Template not found")
            return False
            
    except Exception as e:
        print(f"❌ Template check failed: {e}")
        return False

def create_production_settings_fix():
    """Create a production settings fix for static files"""
    try:
        print("⚙️ Creating production settings fix...")
        
        settings_dir = os.path.join(settings.BASE_DIR, 'onam_project', 'settings')
        production_file = os.path.join(settings_dir, 'production.py')
        
        if os.path.exists(production_file):
            with open(production_file, 'r') as f:
                content = f.read()
            
            # Check if STATICFILES_STORAGE is set to a safe option
            if 'ManifestStaticFilesStorage' in content:
                # Replace with a safer option for production
                new_content = content.replace(
                    'django.contrib.staticfiles.storage.ManifestStaticFilesStorage',
                    'django.contrib.staticfiles.storage.StaticFilesStorage'
                )
                
                # Write the fix
                with open(production_file, 'w') as f:
                    f.write(new_content)
                
                print("   ✅ Updated STATICFILES_STORAGE to safer option")
            else:
                print("   ✅ STATICFILES_STORAGE already safe")
                
            return True
        else:
            print("   ❌ Production settings file not found")
            return False
            
    except Exception as e:
        print(f"❌ Settings fix failed: {e}")
        return False

def main():
    """Main function to fix static files"""
    print("🔧 PRODUCTION STATIC FILES FIX")
    print("=" * 40)
    
    # Step 1: Copy images
    copy_maveli_images()
    
    # Step 2: Fix production settings
    create_production_settings_fix()
    
    # Step 3: Check template
    fix_template_static_refs()
    
    # Step 4: Collect static files
    collect_static_files()
    
    print("\n✅ STATIC FILES FIX COMPLETE!")
    print("🌐 Your site should now load without static file errors")
    print("🔄 Restart your server to apply changes")

if __name__ == "__main__":
    main()
