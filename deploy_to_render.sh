#!/bin/bash
# Render Deployment Script
# This script should be run after the emergency fixes are applied

echo "🚀 Starting Render Deployment..."

# Ensure we're in the right directory
cd /mnt/c/Users/SMADAMBA/OneDrive\ -\ Volvo\ Cars/Documents/Testing/Test/onam-celebration/onam-celebration

# Set environment variables for production
export DJANGO_SETTINGS_MODULE=onam_project.settings.production

# Create logs directory
mkdir -p logs

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create cache table
echo "🗄️ Creating cache table..."
python manage.py createcachetable cache_table || echo "Cache table may already exist"

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate --noinput

# Create superuser if needed
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created')
else:
    print(f'Superuser {username} already exists')
"

# Run basic health check
echo "🏥 Running health check..."
python manage.py check

# Test database connection
echo "🔌 Testing database connection..."
python manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"

echo "✅ Deployment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Push your changes to Git"
echo "2. Deploy to Render"
echo "3. Set environment variables in Render dashboard:"
echo "   - DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST"
echo "   - DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD"
echo "4. Test your application at: https://onam-celebration.onrender.com"
echo "5. Admin access at: https://onam-celebration.onrender.com/custom-admin/"
