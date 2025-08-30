"""
Script to test and fix media file issues in the Onam app.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from apps.core.models import TreasureHuntQuestion, PlayerAnswer


def test_media_serving():
    """Test media file serving and accessibility"""
    print("🔍 Testing Media File Serving...")
    print("=" * 50)
    
    # Check MEDIA settings
    print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"🔗 MEDIA_URL: {settings.MEDIA_URL}")
    
    # Check if MEDIA_ROOT exists
    if os.path.exists(settings.MEDIA_ROOT):
        print(f"✅ MEDIA_ROOT directory exists")
        
        # List subdirectories
        for subdir in ['question_images', 'treasure_hunt_photos', 'avatars']:
            subdir_path = os.path.join(settings.MEDIA_ROOT, subdir)
            if os.path.exists(subdir_path):
                files = os.listdir(subdir_path)
                print(f"  📂 {subdir}: {len(files)} files")
                for file in files[:3]:  # Show first 3 files
                    print(f"    📄 {file}")
                if len(files) > 3:
                    print(f"    ... and {len(files) - 3} more")
            else:
                print(f"  ❌ {subdir}: Directory not found")
    else:
        print(f"❌ MEDIA_ROOT directory does not exist")
    
    print()


def test_question_images():
    """Test question images specifically"""
    print("🖼️  Testing Question Images...")
    print("=" * 50)
    
    questions_with_images = TreasureHuntQuestion.objects.filter(question_image__isnull=False)
    print(f"📊 Questions with images: {questions_with_images.count()}")
    
    for question in questions_with_images:
        print(f"\n🔍 Question {question.order}:")
        print(f"  📄 File: {question.question_image.name}")
        print(f"  🔗 URL: {question.question_image.url}")
        
        # Check if file exists
        if question.question_image:
            file_path = question.question_image.path if hasattr(question.question_image, 'path') else None
            if file_path and os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"  ✅ File exists ({file_size:,} bytes)")
            else:
                print(f"  ❌ File not found on disk")
        else:
            print(f"  ⚠️  No image file attached")


def test_player_photos():
    """Test uploaded player photos"""
    print("📸 Testing Player Photos...")
    print("=" * 50)
    
    answers_with_photos = PlayerAnswer.objects.filter(photo_answer__isnull=False)
    print(f"📊 Answers with photos: {answers_with_photos.count()}")
    
    for answer in answers_with_photos[:5]:  # Show first 5
        print(f"\n🔍 Player: {answer.player.name}, Question: {answer.question.order}")
        print(f"  📄 File: {answer.photo_answer.name}")
        print(f"  🔗 URL: {answer.photo_answer.url}")
        
        # Check Google Photos info
        if answer.google_photos_media_id:
            print(f"  ☁️  Google Photos ID: {answer.google_photos_media_id}")
            print(f"  🌐 Google Photos URL: {answer.google_photos_url}")
        else:
            print(f"  📱 Local storage only")
        
        # Check if file exists
        if answer.photo_answer:
            file_path = answer.photo_answer.path if hasattr(answer.photo_answer, 'path') else None
            if file_path and os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"  ✅ File exists ({file_size:,} bytes)")
            else:
                print(f"  ❌ File not found on disk")


def fix_media_permissions():
    """Fix media directory permissions"""
    print("🔧 Fixing Media Permissions...")
    print("=" * 50)
    
    try:
        # Ensure media directories exist
        media_dirs = [
            settings.MEDIA_ROOT,
            os.path.join(settings.MEDIA_ROOT, 'question_images'),
            os.path.join(settings.MEDIA_ROOT, 'treasure_hunt_photos'),
            os.path.join(settings.MEDIA_ROOT, 'avatars'),
        ]
        
        for dir_path in media_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                print(f"✅ Created directory: {dir_path}")
            else:
                print(f"📁 Directory exists: {dir_path}")
        
        print("\n✅ Media directories are set up correctly")
        
    except Exception as e:
        print(f"❌ Error fixing permissions: {e}")


def create_test_image():
    """Create a test image to verify upload functionality"""
    print("🎨 Creating Test Image...")
    print("=" * 50)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a simple test image
        img = Image.new('RGB', (400, 300), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            # Try to use a system font
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        draw.text((50, 100), "Onam Test Image", fill='darkblue', font=font)
        draw.text((50, 150), "Media serving test", fill='darkblue', font=font)
        
        # Save to media directory
        test_path = os.path.join(settings.MEDIA_ROOT, 'question_images', 'test_image.jpg')
        img.save(test_path, 'JPEG')
        
        print(f"✅ Test image created: {test_path}")
        print(f"🔗 URL would be: {settings.MEDIA_URL}question_images/test_image.jpg")
        
    except ImportError:
        print("⚠️  PIL not available, skipping test image creation")
    except Exception as e:
        print(f"❌ Error creating test image: {e}")


def main():
    """Run all media tests"""
    print("🎯 Onam App - Media File Diagnostics")
    print("=" * 60)
    
    test_media_serving()
    test_question_images()
    test_player_photos()
    fix_media_permissions()
    create_test_image()
    
    print("\n🎉 Media diagnostics complete!")
    print("\n💡 If images still don't load:")
    print("   1. Check Django DEBUG setting")
    print("   2. Verify web server configuration")
    print("   3. Check browser developer console for 404 errors")
    print("   4. Ensure MEDIA_URL is correctly configured")


if __name__ == "__main__":
    main()
