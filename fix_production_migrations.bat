@echo off
REM Production Migration Fix Script for Windows
echo === Onam Celebration - Production Migration Fix ===
echo This script will apply all missing migrations to fix the leaderboard.
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if manage.py exists
if not exist "manage.py" (
    echo ❌ Error: manage.py not found. Make sure you're in the project root.
    pause
    exit /b 1
)

echo ✓ Found manage.py in current directory

REM Show current migration status
echo.
echo === Current Migration Status ===
python manage.py showmigrations core

echo.
echo === Applying Missing Migrations ===

REM Apply individual migrations in order
echo ^>^>^> Applying migration 0010 (Individual Event Models)...
python manage.py migrate core 0010
if %errorlevel% equ 0 (
    echo ✓ Migration 0010 applied successfully
) else (
    echo ⚠ Warning: Migration 0010 failed or already applied
)

echo.
echo ^>^>^> Applying migration 0011 (Fix Individual Vote Null Fields)...
python manage.py migrate core 0011
if %errorlevel% equ 0 (
    echo ✓ Migration 0011 applied successfully
) else (
    echo ⚠ Warning: Migration 0011 failed or already applied
)

echo.
echo ^>^>^> Applying migration 0012 (Team Event Participation)...
python manage.py migrate core 0012
if %errorlevel% equ 0 (
    echo ✓ Migration 0012 applied successfully
) else (
    echo ⚠ Warning: Migration 0012 failed or already applied
)

echo.
echo ^>^>^> Applying any remaining migrations...
python manage.py migrate
if %errorlevel% equ 0 (
    echo ✓ All migrations applied successfully
) else (
    echo ⚠ Warning: Some migrations may have failed
)

REM Show final status
echo.
echo === Final Migration Status ===
python manage.py showmigrations core

echo.
echo === Testing Database Tables ===

REM Test if we can access the new models
python -c "import os; import django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base'); django.setup(); from apps.core.models import IndividualEventScore, TeamEventParticipation, IndividualParticipation, IndividualEventVote; print('✅ Database Test Results:'); print(f'   IndividualEventScore records: {IndividualEventScore.objects.count()}'); print(f'   TeamEventParticipation records: {TeamEventParticipation.objects.count()}'); print(f'   IndividualParticipation records: {IndividualParticipation.objects.count()}'); print(f'   IndividualEventVote records: {IndividualEventVote.objects.count()}'); print(''); print('🎉 All models are accessible! The leaderboard should now work.')"

if %errorlevel% neq 0 (
    echo ❌ Database test failed. The migrations may not have been applied correctly.
)

echo.
echo === Migration Fix Complete ===
echo If all tests passed, you can now:
echo 1. Restart your Django development server
echo 2. Visit the leaderboard page  
echo 3. The Malayalam branding and Maveli images should be visible
echo 4. Individual and team scoring should work properly
echo.
echo If there are still errors, check the Django logs for details.
echo.
pause
