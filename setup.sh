#!/bin/bash

# Onam Project Setup Script
# This script sets up the Django project environment and handles externally-managed-environment issues

set -e

echo "🌸 Setting up Onam Celebration & Treasure Hunt Project 🌸"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check for externally managed environment and install venv if needed
echo "🔍 Checking Python environment..."
if ! python3 -m venv --help &> /dev/null; then
    echo "⚠️ python3-venv not found. Installing..."
    
    # Try different package managers
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3-venv python3-full
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-venv
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-venv
    else
        echo "❌ Could not install python3-venv. Please install it manually."
        exit 1
    fi
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p media/avatars
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images

# Copy environment file
echo "⚙️ Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file. Please update it with your configuration."
fi

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "👑 Creating superuser..."
echo "Do you want to create a superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Load initial data (optional)
echo "📊 Loading sample data..."
python manage.py loaddata fixtures/sample_data.json || echo "No sample data found, skipping..."

echo ""
echo "🎉 Setup complete! 🎉"
echo ""
echo "To start the development server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "To access the admin panel:"
echo "  http://localhost:8000/admin/"
echo ""
echo "To start the treasure hunt:"
echo "  http://localhost:8000/"
echo ""
echo "Happy Onam! ഓണാശംസകൾ! 🌸"
