@echo off
echo 🔗 Google Photos Integration Setup for Onam App
echo ==================================================

echo Step 1: Checking current setup...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    pause
    exit /b 1
) else (
    echo ✅ Python is available
)

REM Check Django
python -c "import django" 2>nul
if errorlevel 1 (
    echo ❌ Django not found
    pause
    exit /b 1
) else (
    echo ✅ Django is available
)

echo.
echo Step 2: Installing Google Photos API dependencies...

pip install google-auth google-auth-oauthlib google-api-python-client google-auth-httplib2
if errorlevel 1 (
    echo ❌ Failed to install packages
    pause
    exit /b 1
) else (
    echo ✅ Packages installed successfully
)

echo.
echo Step 3: Checking Google Photos integration status...

python manage.py enable_google_photos --status

echo.
echo Step 4: Setting up environment variables...

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    type nul > .env
)

REM Add Google Photos settings if they don't exist
findstr /C:"GOOGLE_PHOTOS_ENABLED" .env >nul 2>&1
if errorlevel 1 (
    echo GOOGLE_PHOTOS_ENABLED=True >> .env
    echo ✅ Added GOOGLE_PHOTOS_ENABLED=True to .env
)

findstr /C:"GOOGLE_PHOTOS_ALBUM_ID" .env >nul 2>&1
if errorlevel 1 (
    echo GOOGLE_PHOTOS_ALBUM_ID=your_album_id_here >> .env
    echo ⚠️  Added placeholder GOOGLE_PHOTOS_ALBUM_ID to .env - update with your actual album ID
)

echo.
echo Step 5: Creating media directories...

if not exist "media\treasure_hunt_photos" mkdir "media\treasure_hunt_photos"
if not exist "media\question_images" mkdir "media\question_images"
if not exist "media\avatars" mkdir "media\avatars"
echo ✅ Media directories created

echo.
echo Step 6: Setup instructions...
echo.
echo 📝 To complete Google Photos integration:
echo.
echo 1. Go to Google Cloud Console: https://console.cloud.google.com/
echo 2. Create a new project or select existing one
echo 3. Enable the 'Photos Library API'
echo 4. Go to 'Credentials' and create 'OAuth 2.0 Client ID'
echo 5. Choose 'Desktop application' as application type
echo 6. Download the JSON credentials file
echo 7. Save it as 'google_photos_credentials.json' in your project root
echo 8. Create a Google Photos album and get its ID from the share URL
echo 9. Update GOOGLE_PHOTOS_ALBUM_ID in your .env file
echo.

echo Step 7: Running diagnostics...

if exist "test_media_fix.py" (
    echo Running media diagnostics...
    python test_media_fix.py
)

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Place your Google Photos credentials file in the project root
echo 2. Update the GOOGLE_PHOTOS_ALBUM_ID in .env
echo 3. Run: python manage.py enable_google_photos --test
echo 4. Start your Django server: python manage.py runserver
echo.
echo For troubleshooting, check the logs in Django admin or console output.
echo.
pause
