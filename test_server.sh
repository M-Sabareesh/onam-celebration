#!/bin/bash

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
