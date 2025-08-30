#!/bin/bash
"""
Startup script for Render.com deployment
This script runs automatically when your app starts on Render
"""

echo "🚀 Starting Onam Celebration App on Render..."

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate

# Check if we need to restore data
echo "🔍 Checking if data restore is needed..."

# Check if questions exist (core structure)
QUESTIONS_COUNT=$(python manage.py shell -c "from apps.core.models import TreasureHuntQuestion; print(TreasureHuntQuestion.objects.count())")

if [ "$QUESTIONS_COUNT" = "0" ]; then
    echo "📥 No questions found. Restoring data from GitHub..."
    
    # Restore structure only (questions and events)
    python manage.py restore_data --structure-only
    
    if [ $? -eq 0 ]; then
        echo "✅ Data restoration completed successfully!"
    else
        echo "⚠️  Data restoration failed. Creating default questions..."
        python manage.py populate_questions
    fi
else
    echo "✅ Questions already exist. Skipping data restore."
fi

# Create superuser if it doesn't exist (for admin access)
echo "👤 Setting up admin user..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os
if not User.objects.filter(is_superuser=True).exists():
    admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'OnamAdmin')
    admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    User.objects.create_superuser(admin_username, 'admin@onam-celebration.com', admin_password)
    print('✅ Admin user created: ' + admin_username + ' / ' + admin_password)
else:
    print('✅ Admin user already exists')
"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🎉 Startup completed! Onam Celebration is ready!"
echo "🌐 Access your app at the Render URL"
echo "👨‍💼 Admin panel: /admin/ (username: admin)"

# Start the application
echo "🚀 Starting Gunicorn server..."
python manage.py runserver 0.0.0.0:$PORT
