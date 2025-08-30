@echo off
echo 🚀 Starting Onam App Test Server
echo =================================

REM Activate virtual environment if it exists
if exist ".venv" (
    echo 📦 Activating virtual environment...
    call .venv\Scripts\activate.bat
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
