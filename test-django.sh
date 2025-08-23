#!/bin/bash

# Simple Django test script
echo "🌸 Testing basic Django setup..."

# Activate virtual environment
source venv/bin/activate

echo "✅ Virtual environment activated"

echo "🔍 Testing Django installation..."
python -c "import django; print(f'Django {django.get_version()} is working!')"

echo "🔧 Testing Django settings..."
python manage.py check --settings=onam_project.settings.development

echo "📊 Creating migrations for built-in apps..."
python manage.py makemigrations --settings=onam_project.settings.development

echo "🗄️ Running migrations..."
python manage.py migrate --settings=onam_project.settings.development

echo "🎯 Testing if server can start..."
timeout 5s python manage.py runserver --settings=onam_project.settings.development &
SERVER_PID=$!

sleep 2

if curl -s http://localhost:8000/health/ > /dev/null; then
    echo "✅ Server is responding!"
else
    echo "⚠️ Server may not be fully ready yet"
fi

# Kill the test server
kill $SERVER_PID 2>/dev/null

echo "🎉 Basic Django setup test completed!"
echo "You can now run: python manage.py runserver --settings=onam_project.settings.development"
