#!/usr/bin/env python3
"""
Simple media file diagnostics without Django dependencies.
"""

import os
import sys
from pathlib import Path

def check_media_files():
    """Check media files and directory structure"""
    print("🔍 Media File Diagnostics")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📂 Current directory: {current_dir}")
    
    # Check for media directory
    media_dir = current_dir / "media"
    if media_dir.exists():
        print(f"✅ Media directory exists: {media_dir}")
        
        # Check subdirectories
        subdirs = ["question_images", "treasure_hunt_photos", "avatars"]
        for subdir in subdirs:
            subdir_path = media_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.glob("*"))
                image_files = [f for f in files if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']]
                print(f"  📁 {subdir}: {len(image_files)} image files")
                
                # Show first few files
                for i, file in enumerate(image_files[:3]):
                    size = file.stat().st_size if file.exists() else 0
                    print(f"    📄 {file.name} ({size:,} bytes)")
                
                if len(image_files) > 3:
                    print(f"    ... and {len(image_files) - 3} more files")
            else:
                print(f"  ❌ {subdir}: Directory not found")
                # Create the directory
                subdir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✅ Created directory: {subdir_path}")
    else:
        print(f"❌ Media directory not found: {media_dir}")
        # Create media directory structure
        media_dir.mkdir(exist_ok=True)
        for subdir in ["question_images", "treasure_hunt_photos", "avatars"]:
            (media_dir / subdir).mkdir(exist_ok=True)
        print("✅ Created media directory structure")

def check_django_setup():
    """Check Django setup without importing Django"""
    print("\n🐍 Django Setup Check")
    print("=" * 50)
    
    # Check for manage.py
    if Path("manage.py").exists():
        print("✅ manage.py found")
    else:
        print("❌ manage.py not found")
        return False
    
    # Check for settings module
    settings_dir = Path("onam_project/settings")
    if settings_dir.exists():
        print("✅ Settings directory found")
        
        # List settings files
        settings_files = list(settings_dir.glob("*.py"))
        for file in settings_files:
            print(f"  📄 {file.name}")
    else:
        print("❌ Settings directory not found")
    
    # Check requirements.txt
    if Path("requirements.txt").exists():
        print("✅ requirements.txt found")
        
        # Check for Google Photos packages
        with open("requirements.txt", "r") as f:
            content = f.read()
            google_packages = [
                "google-api-python-client",
                "google-auth",
                "google-auth-oauthlib"
            ]
            
            for package in google_packages:
                if package in content:
                    print(f"  ✅ {package} in requirements")
                else:
                    print(f"  ❌ {package} missing from requirements")
    else:
        print("❌ requirements.txt not found")

def check_image_file(image_path):
    """Check if an image file is valid"""
    if not os.path.exists(image_path):
        return False, "File not found"
    
    try:
        # Check file size
        size = os.path.getsize(image_path)
        if size == 0:
            return False, "File is empty"
        
        # Check if it's an image (basic check)
        with open(image_path, 'rb') as f:
            header = f.read(8)
            
        # Check common image file signatures
        if header.startswith(b'\xff\xd8\xff'):  # JPEG
            return True, f"Valid JPEG ({size:,} bytes)"
        elif header.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
            return True, f"Valid PNG ({size:,} bytes)"
        elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):  # GIF
            return True, f"Valid GIF ({size:,} bytes)"
        else:
            return False, f"Unknown format ({size:,} bytes)"
            
    except Exception as e:
        return False, f"Error reading file: {e}"

def test_specific_image():
    """Test the specific image mentioned in the issue"""
    print("\n🖼️  Testing Specific Image")
    print("=" * 50)
    
    # Test the specific image mentioned: IMG_9164.JPG
    test_files = [
        "media/question_images/IMG_9164.JPG",
        "media/question_images/Onma5.jpg",
        "media/treasure_hunt_photos/IMG_7077.JPG",
        "media/treasure_hunt_photos/IMG_7457.JPG",
    ]
    
    for file_path in test_files:
        if Path(file_path).exists():
            is_valid, message = check_image_file(file_path)
            status = "✅" if is_valid else "❌"
            print(f"{status} {file_path}: {message}")
            
            # Show expected URL
            url_path = file_path.replace("media/", "/media/")
            print(f"   🔗 Expected URL: {url_path}")
        else:
            print(f"❌ {file_path}: File not found")

def create_test_environment():
    """Create a test environment setup"""
    print("\n🧪 Environment Setup")
    print("=" * 50)
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file exists")
        
        # Check for Google Photos settings
        with open(env_file, "r") as f:
            content = f.read()
            
        settings_to_check = [
            "GOOGLE_PHOTOS_ENABLED",
            "GOOGLE_PHOTOS_ALBUM_ID",
            "DEBUG"
        ]
        
        for setting in settings_to_check:
            if setting in content:
                # Extract the value
                for line in content.split('\n'):
                    if line.startswith(setting):
                        print(f"  📋 {line}")
                        break
            else:
                print(f"  ❌ {setting} not found in .env")
    else:
        print("❌ .env file not found")
        
        # Create basic .env file
        basic_env = """# Onam Celebration App Environment
DEBUG=True
GOOGLE_PHOTOS_ENABLED=False
GOOGLE_PHOTOS_ALBUM_ID=your_album_id_here
DJANGO_SECRET_KEY=dev-secret-key-change-in-production
"""
        with open(".env", "w") as f:
            f.write(basic_env)
        print("✅ Created basic .env file")

def main():
    """Run all diagnostics"""
    print("🎯 Onam App - Quick Diagnostics")
    print("=" * 60)
    
    check_media_files()
    check_django_setup()
    test_specific_image()
    create_test_environment()
    
    print("\n💡 Summary & Next Steps:")
    print("=" * 50)
    print("1. ✅ Media directories are set up")
    print("2. 🔧 To fix image loading:")
    print("   - Ensure Django DEBUG=True for development")
    print("   - Check URL configuration includes media serving")
    print("   - Verify file permissions")
    print("3. 🔗 For Google Photos integration:")
    print("   - Install: pip install google-api-python-client google-auth google-auth-oauthlib")
    print("   - Set up Google Cloud Console project")
    print("   - Download credentials JSON file")
    print("   - Update GOOGLE_PHOTOS_ENABLED=True in .env")
    print("\n4. 🚀 To test: python manage.py runserver")
    print("   Then visit: http://localhost:8000/media/question_images/Onma5.jpg")

if __name__ == "__main__":
    main()
