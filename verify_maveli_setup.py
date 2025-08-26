#!/usr/bin/env python
"""
Verify Maveli Images Setup
This script checks that everything is properly configured for the Maveli images.
"""

import os
from pathlib import Path

def check_maveli_images():
    """Check if Maveli images are in the correct locations"""
    print("🔍 Checking Maveli Images Setup...")
    
    # Check static/images directory
    static_images = Path('static/images')
    media_maveli = Path('media/Maveli')
    
    maveli_files = ['Maveli.jpg', 'Maveli2.jpg', 'Maveli2.png', 'Maveli4.jpg']
    
    print(f"\n📁 Static Images Directory: {static_images}")
    static_found = 0
    for img in maveli_files:
        static_path = static_images / img
        if static_path.exists():
            size = static_path.stat().st_size
            print(f"  ✅ {img} ({size:,} bytes)")
            static_found += 1
        else:
            print(f"  ❌ {img} (missing)")
    
    print(f"\n📁 Media Maveli Directory: {media_maveli}")
    media_found = 0
    for img in maveli_files:
        media_path = media_maveli / img
        if media_path.exists():
            size = media_path.stat().st_size
            print(f"  ✅ {img} ({size:,} bytes)")
            media_found += 1
        else:
            print(f"  ❌ {img} (missing)")
    
    return static_found, media_found

def check_template():
    """Check if template is properly configured"""
    print(f"\n🔍 Checking Template Configuration...")
    
    template_path = Path('templates/core/index.html')
    if template_path.exists():
        content = template_path.read_text(encoding='utf-8')
        
        if 'static \'images/Maveli.jpg\'' in content:
            print("  ✅ Template references static Maveli.jpg")
        else:
            print("  ❌ Template doesn't reference static Maveli.jpg")
        
        if 'onerror=' in content:
            print("  ✅ Template has error handling for missing images")
        else:
            print("  ❌ Template lacks error handling")
            
        if '🤴🏾' in content:
            print("  ✅ Template has emoji fallback")
        else:
            print("  ❌ Template lacks emoji fallback")
    else:
        print("  ❌ Template file not found")

def main():
    """Main function"""
    print("🖼️  Maveli Images Setup Verification")
    print("=" * 40)
    
    static_count, media_count = check_maveli_images()
    check_template()
    
    print(f"\n📊 Summary:")
    print(f"  Static images found: {static_count}/4")
    print(f"  Media images found: {media_count}/4")
    
    if static_count == 4:
        print("\n🎉 SUCCESS! All Maveli images are properly set up!")
        print("\n✅ Next steps:")
        print("1. Run: python manage.py collectstatic --noinput")
        print("2. Test locally: python manage.py runserver")
        print("3. Deploy to production")
        print("\n🌟 Your website will now show beautiful Maveli images!")
    elif static_count > 0:
        print(f"\n⚠️  PARTIAL SUCCESS: {static_count} images found in static/")
        print("Some images may be missing, but the site should work with fallbacks.")
    else:
        print("\n❌ No static images found. Please copy images from media/ to static/images/")
        print("\nCommands to run:")
        print("Windows: copy \"media\\Maveli\\*.*\" \"static\\images\\\"")
        print("Linux/Mac: cp media/Maveli/*.* static/images/")

if __name__ == '__main__':
    main()
