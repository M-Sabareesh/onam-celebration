@echo off
REM Onam Project Setup Script for Windows
REM This script sets up the Django project environment

echo 🌸 Setting up Onam Celebration & Treasure Hunt Project 🌸

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo 📁 Creating directories...
if not exist logs mkdir logs
if not exist media\avatars mkdir media\avatars
if not exist static\css mkdir static\css
if not exist static\js mkdir static\js
if not exist static\images mkdir static\images

REM Copy environment file
echo ⚙️ Setting up environment...
if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file. Please update it with your configuration.
)

REM Run migrations
echo 🗄️ Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser (optional)
echo 👑 Do you want to create a superuser? (y/n)
set /p create_superuser=
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

REM Collect static files
echo 🎨 Collecting static files...
python manage.py collectstatic --noinput

REM Load initial data (optional)
echo 📊 Loading sample data...
python manage.py loaddata fixtures/sample_data.json 2>nul || echo No sample data found, skipping...

echo.
echo 🎉 Setup complete! 🎉
echo.
echo To start the development server:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo To access the admin panel:
echo   http://localhost:8000/admin/
echo.
echo To start the treasure hunt:
echo   http://localhost:8000/
echo.
echo Happy Onam! ഓണാശംസകൾ! 🌸
pause
