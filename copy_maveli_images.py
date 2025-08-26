#!/usr/bin/env python
"""
Copy Maveli Images from Media to Static
This script copies Maveli images to the correct static location for production use.
"""

import shutil
from pathlib import Path

def copy_maveli_images():
    """Copy Maveli images from media to static directory"""
    print("🖼️  Copying Maveli images from media to static...")
    
    # Define paths
    project_root = Path(__file__).parent
    media_maveli = project_root / 'media' / 'Maveli'
    static_images = project_root / 'static' / 'images'
    
    # Ensure static/images directory exists
    static_images.mkdir(parents=True, exist_ok=True)
    
    # List of Maveli images to copy
    maveli_images = ['Maveli.jpg', 'Maveli2.jpg', 'Maveli2.png', 'Maveli4.jpg']
    
    copied_count = 0
    for img_name in maveli_images:
        source = media_maveli / img_name
        destination = static_images / img_name
        
        if source.exists():
            try:
                shutil.copy2(source, destination)
                print(f"✅ Copied {img_name} -> static/images/")
                copied_count += 1
            except Exception as e:
                print(f"❌ Failed to copy {img_name}: {e}")
        else:
            print(f"⚠️  {img_name} not found in media/Maveli/")
    
    print(f"\n🎉 Successfully copied {copied_count} Maveli images!")
    return copied_count > 0

def main():
    """Main function"""
    print("📁 Maveli Images Setup")
    print("=" * 30)
    
    if copy_maveli_images():
        print("\n✅ Maveli images are now ready for static file serving!")
        print("\nNext steps:")
        print("1. Update the template to use the real images")
        print("2. Run: python manage.py collectstatic")
        print("3. Deploy to production")
    else:
        print("\n❌ No images were copied. Check the media/Maveli/ directory.")

if __name__ == '__main__':
    main()
