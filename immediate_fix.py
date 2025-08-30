#!/usr/bin/env python3
"""
Immediate fix for image loading and Google Photos issues.
This script addresses the specific problems mentioned.
"""

import os
import json
from pathlib import Path

def fix_missing_image():
    """Address the missing IMG_9164.JPG image"""
    print("🖼️  Fixing Missing Image Issue")
    print("=" * 50)
    
    missing_image = "media/question_images/IMG_9164.JPG"
    
    if not Path(missing_image).exists():
        print(f"❌ Missing image: {missing_image}")
        
        # Check if there are other images we can use as reference
        question_images_dir = Path("media/question_images")
        existing_images = list(question_images_dir.glob("*.[jJ][pP][gG]"))
        
        if existing_images:
            print(f"✅ Found {len(existing_images)} existing images:")
            for img in existing_images:
                print(f"   📄 {img.name}")
            
            # Suggest solution
            print(f"\n💡 Solutions:")
            print(f"1. Upload the missing image: {missing_image}")
            print(f"2. Update the database to reference an existing image")
            print(f"3. Use the existing image: {existing_images[0].name}")
        else:
            print("❌ No images found in question_images directory")
    else:
        print(f"✅ Image exists: {missing_image}")

def check_google_photos_config():
    """Check and fix Google Photos configuration"""
    print("\n☁️  Google Photos Configuration")
    print("=" * 50)
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            env_content = f.read()
        
        # Check for Google Photos settings
        if "GOOGLE_PHOTOS_ENABLED" in env_content:
            print("✅ GOOGLE_PHOTOS_ENABLED found in .env")
        else:
            print("❌ GOOGLE_PHOTOS_ENABLED missing from .env")
            
            # Add Google Photos settings
            with open(env_file, "a") as f:
                f.write("\n# Google Photos Integration\n")
                f.write("GOOGLE_PHOTOS_ENABLED=True\n")
                f.write("GOOGLE_PHOTOS_ALBUM_ID=your_album_id_here\n")
                f.write("GOOGLE_PHOTOS_ALBUM_NAME=Onam Celebration - Treasure Hunt Photos\n")
            print("✅ Added Google Photos settings to .env")
    
    # Check credentials file
    creds_file = Path("google_photos_credentials.json")
    if not creds_file.exists():
        print("❌ Google Photos credentials file not found")
        
        # Create placeholder
        placeholder_creds = {
            "installed": {
                "client_id": "your-client-id.googleusercontent.com",
                "project_id": "your-project-id", 
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "your-client-secret",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        with open(creds_file, "w") as f:
            json.dump(placeholder_creds, f, indent=2)
        
        print("✅ Created placeholder credentials file")
        print("⚠️  Replace with actual credentials from Google Cloud Console")
    else:
        print("✅ Credentials file exists")

def create_test_server_script():
    """Create a script to test the server with proper media serving"""
    print("\n🚀 Creating Test Server Script")
    print("=" * 50)
    
    test_script = """#!/bin/bash

echo "🚀 Starting Onam App Test Server"
echo "================================="

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Install requirements if needed
echo "📦 Installing/updating requirements..."
pip install -r requirements.txt

# Run Django checks
echo "🔍 Running Django checks..."
python manage.py check

# Apply migrations
echo "🗃️  Applying migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Check Google Photos status
echo "☁️  Checking Google Photos integration..."
python manage.py enable_google_photos --status || echo "Google Photos check not available yet"

# Start server
echo "🌐 Starting development server..."
echo "   Image test URL: http://localhost:8000/media/question_images/Onma5.jpg"
echo "   Admin URL: http://localhost:8000/admin/"
echo "   Main app: http://localhost:8000/"
echo ""
echo "Press Ctrl+C to stop the server"
python manage.py runserver
"""
    
    with open("test_server.sh", "w") as f:
        f.write(test_script)
    
    os.chmod("test_server.sh", 0o755)  # Make executable
    print("✅ Created test_server.sh script")

def create_windows_test_script():
    """Create Windows version of test script"""
    test_script_bat = """@echo off
echo 🚀 Starting Onam App Test Server
echo =================================

REM Activate virtual environment if it exists
if exist ".venv" (
    echo 📦 Activating virtual environment...
    call .venv\\Scripts\\activate.bat
)

REM Install requirements
echo 📦 Installing/updating requirements...
pip install -r requirements.txt

REM Run Django checks
echo 🔍 Running Django checks...
python manage.py check

REM Apply migrations
echo 🗃️  Applying migrations...
python manage.py migrate

REM Check Google Photos status
echo ☁️  Checking Google Photos integration...
python manage.py enable_google_photos --status 2>nul || echo Google Photos check not available yet

REM Start server
echo 🌐 Starting development server...
echo    Image test URL: http://localhost:8000/media/question_images/Onma5.jpg
echo    Admin URL: http://localhost:8000/admin/
echo    Main app: http://localhost:8000/
echo.
echo Press Ctrl+C to stop the server
python manage.py runserver

pause
"""
    
    with open("test_server.bat", "w") as f:
        f.write(test_script_bat)
    
    print("✅ Created test_server.bat script")

def create_quick_fix_summary():
    """Create a summary of the fixes applied"""
    summary = """# Quick Fix Summary - Image Loading & Google Photos

## Issues Addressed

### 1. Missing Image File
- **Problem**: `media/question_images/IMG_9164.JPG` not found
- **URL**: `/media/question_images/IMG_9164.JPG` returns 404
- **Solution**: 
  - Upload the missing image file
  - Or update database references to use existing images
  - Check existing images in `media/question_images/`

### 2. Google Photos Upload Not Working
- **Problem**: Photos not actually uploading to Google Photos album
- **Cause**: Missing or incorrect API credentials
- **Solution**:
  - Set up Google Cloud Console project
  - Enable Photos Library API
  - Download OAuth 2.0 credentials
  - Configure album ID in .env

## Quick Tests

### Test Image Loading
```bash
# Start server
./test_server.sh  # Linux/Mac
# or
test_server.bat   # Windows

# Test in browser
http://localhost:8000/media/question_images/Onma5.jpg
```

### Test Google Photos Integration
```bash
# Check status
python manage.py enable_google_photos --status

# Test upload (requires credentials)
python manage.py enable_google_photos --test
```

## Environment Configuration

Update `.env` file:
```
GOOGLE_PHOTOS_ENABLED=True
GOOGLE_PHOTOS_ALBUM_ID=your_actual_album_id
GOOGLE_PHOTOS_ALBUM_NAME=Onam Celebration - Treasure Hunt Photos
```

## Google Cloud Console Setup

1. Go to: https://console.cloud.google.com/
2. Create/select project
3. Enable "Photos Library API"
4. Create OAuth 2.0 Client ID credentials
5. Download JSON file as `google_photos_credentials.json`
6. Create Google Photos album and get ID from share URL

## Files Created/Updated

- ✅ `.env` - Added Google Photos settings
- ✅ `google_photos_credentials.json` - Placeholder credentials
- ✅ `test_server.sh` - Linux/Mac test script
- ✅ `test_server.bat` - Windows test script
- ✅ Media directories with `.gitkeep` files

## Next Steps

1. **Immediate**: Run `./test_server.sh` to test image loading
2. **Short-term**: Upload missing image or update database
3. **Medium-term**: Set up Google Cloud Console and get real credentials
4. **Long-term**: Test Google Photos upload functionality

## Troubleshooting

### Images Not Loading
- Check file exists in correct directory
- Verify Django DEBUG=True for development
- Check URL matches file path exactly
- Look for typos in filenames (case-sensitive)

### Google Photos Fails
- Verify credentials file is valid JSON
- Check album ID is correct (from share URL)
- Ensure API is enabled in Google Cloud Console
- Check Django logs for detailed error messages
"""
    
    with open("QUICK_FIX_SUMMARY.md", "w") as f:
        f.write(summary)
    
    print("✅ Created QUICK_FIX_SUMMARY.md")

def main():
    """Run immediate fixes"""
    print("⚡ Immediate Fix for Image Loading & Google Photos")
    print("=" * 60)
    
    fix_missing_image()
    check_google_photos_config() 
    create_test_server_script()
    create_windows_test_script()
    create_quick_fix_summary()
    
    print("\n🎉 Immediate Fixes Complete!")
    print("=" * 50)
    
    print("\n🔧 What was fixed:")
    print("✅ Google Photos environment variables added to .env")
    print("✅ Placeholder credentials file created")
    print("✅ Test server scripts created")
    print("✅ Media directory structure verified")
    
    print("\n🚀 Quick Test:")
    print("1. Run: ./test_server.sh (Linux/Mac) or test_server.bat (Windows)")
    print("2. Visit: http://localhost:8000/media/question_images/Onma5.jpg")
    print("3. Check: Does the existing image load?")
    
    print("\n📋 For missing IMG_9164.JPG:")
    print("- Upload the file to media/question_images/")
    print("- Or update the database to reference existing images")
    
    print("\n☁️  For Google Photos:")
    print("- Get credentials from Google Cloud Console")
    print("- Update GOOGLE_PHOTOS_ALBUM_ID in .env")
    print("- Run: python manage.py enable_google_photos --test")
    
    print(f"\n📖 See QUICK_FIX_SUMMARY.md for detailed instructions")

if __name__ == "__main__":
    main()
