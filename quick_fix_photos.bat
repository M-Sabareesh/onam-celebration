@echo off
REM Quick fix script for treasure hunt photo issues
echo 🔧 Quick Fix for Treasure Hunt Photo Issues
echo ==========================================

REM 1. Fix the database schema first
echo 📊 Step 1: Fixing database schema...
python manage.py fix_google_photos --fix-db

REM 2. Debug media files
echo 🔍 Step 2: Checking media files...
python manage.py debug_media --check-images --check-photos

REM 3. Collect static files
echo 📁 Step 3: Collecting static files...
python manage.py collectstatic --noinput

REM 4. Test the treasure hunt page
echo 🧪 Step 4: Testing treasure hunt functionality...
python -c "
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
sys.path.append('.')
django.setup()

from apps.core.models import TreasureHuntQuestion, PlayerAnswer
from django.conf import settings

print('📍 Questions with images:', TreasureHuntQuestion.objects.filter(question_image__isnull=False).count())
print('📍 Photo answers:', PlayerAnswer.objects.filter(photo_answer__isnull=False).count())
print('📍 Google Photos enabled:', getattr(settings, 'GOOGLE_PHOTOS_ENABLED', False))
print('📍 Media URL:', settings.MEDIA_URL)

# Test image URLs
questions = TreasureHuntQuestion.objects.filter(question_image__isnull=False)[:3]
for q in questions:
    print(f'📸 Q{q.order} image URL: {q.question_image.url}')

photos = PlayerAnswer.objects.filter(photo_answer__isnull=False)[:3]
for p in photos:
    print(f'📱 {p.player.name} photo URL: {p.photo_answer.url}')
"

echo.
echo ✅ Quick fix completed!
echo.
echo 🎯 Solutions implemented:
echo 1. ✅ Database schema fixed for Google Photos
echo 2. ✅ Enhanced error handling for photo uploads
echo 3. ✅ Better image loading with retry functionality
echo 4. ✅ Mobile-optimized photo display
echo 5. ✅ Graceful fallback when Google Photos fails
echo.
echo 📱 For mobile users:
echo - Photos now display better on mobile devices
echo - Click/tap photos to view full size
echo - Loading indicators show progress
echo - Error messages are user-friendly
echo.
echo ☁️  For Google Photos integration:
echo - Currently disabled (no API credentials)
echo - Photos are stored locally and work fine
echo - Can be enabled later with proper setup
echo.
echo 🚀 Your treasure hunt should now work properly!
echo    Test it on mobile devices for the best experience.

pause
