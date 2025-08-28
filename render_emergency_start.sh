#!/bin/bash
# Simple Render Start Command with Migration Fix
# Use this as the start command in Render

echo "🚨 EMERGENCY MIGRATION FIX"
echo "Target: Fix missing core_simpleeventscore table"

# Run migrations with force
echo "🔧 Running migrations..."
python manage.py migrate --noinput

# If core migration fails, try to apply just the missing one
echo "🔧 Ensuring SimpleEventScore migration..."
python manage.py migrate core 0015_simple_event_scoring --noinput || echo "Migration already applied or failed"

# Collect static files
echo "🔧 Collecting static files..."
python manage.py collectstatic --noinput || echo "Static collection failed but continuing"

# Create media directories
echo "🔧 Creating media directories..."
mkdir -p media/question_images
mkdir -p media/treasure_hunt_photos  
mkdir -p media/avatars

# Start server
echo "🌐 Starting server..."
exec gunicorn onam_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
