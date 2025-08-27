@echo off
REM Chart Color Fix Script for Windows
echo 🎨 Fixing Chart Colors Issue
echo ==================================

REM 1. Check if static files directory exists
if exist "static\js" (
    echo ✅ Static JS directory exists
) else (
    echo ❌ Creating static JS directory
    mkdir static\js
)

REM 2. Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

REM 3. Check chart.js file
if exist "static\js\leaderboard_chart.js" (
    echo ✅ Chart JavaScript file exists
) else (
    echo ❌ Chart JavaScript file missing
)

echo.
echo 💡 To fix chart colors:
echo 1. Check browser console for JavaScript errors
echo 2. Verify Chart.js CDN loads correctly
echo 3. Ensure static files are served properly
echo 4. Check template rendering of chart_data
echo.
echo 🔧 Manual verification steps:
echo 1. Open browser dev tools on leaderboard page
echo 2. Look for console log messages from chart initialization
echo 3. Check Network tab for 404 errors on static files
echo 4. Verify chart_data contains color properties

pause
