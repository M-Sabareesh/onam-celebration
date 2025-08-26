@echo off
echo 🖼️  Copying Maveli images from media to static...

REM Create static/images directory if it doesn't exist
if not exist "static\images" mkdir "static\images"

REM Copy Maveli images from media to static
if exist "media\Maveli\Maveli.jpg" (
    copy "media\Maveli\*.jpg" "static\images\" >nul 2>&1
    copy "media\Maveli\*.png" "static\images\" >nul 2>&1
    echo ✅ Copied Maveli images to static/images/
) else (
    echo ❌ Maveli images not found in media/Maveli/
)

REM List what we have now
echo.
echo 📁 Contents of static/images/:
dir "static\images" /b

echo.
echo 🎉 Maveli images setup complete!
echo.
echo Next steps:
echo 1. Run: python manage.py collectstatic
echo 2. Test the website locally
echo 3. Deploy to production

pause
