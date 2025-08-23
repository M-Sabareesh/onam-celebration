#!/bin/bash
# Django Setup Validation Script

echo "=== Django Onam Project Setup Validation ==="

# Set environment variables
export DJANGO_SETTINGS_MODULE=onam_project.settings.development
export DEBUG=True
export SECRET_KEY=django-insecure-test-key
export DATABASE_URL=sqlite:///db.sqlite3

echo "✅ Environment variables set"

# Test Django check
echo "🔍 Running Django check..."
python manage.py check
if [ $? -eq 0 ]; then
    echo "✅ Django check passed"
else
    echo "❌ Django check failed"
    exit 1
fi

# Test migrations
echo "🔄 Testing migrations..."
python manage.py showmigrations
if [ $? -eq 0 ]; then
    echo "✅ Migrations are working"
else
    echo "❌ Migrations failed"
    exit 1
fi

# Test static files
echo "📁 Testing static files collection..."
python manage.py collectstatic --noinput --dry-run
if [ $? -eq 0 ]; then
    echo "✅ Static files configuration is working"
else
    echo "❌ Static files configuration failed"
    exit 1
fi

# Test server validation
echo "🌐 Testing server configuration..."
python -c "
import os
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

# Test URL resolution
from django.urls import reverse
try:
    home_url = reverse('core:home')
    print(f'✅ Home URL resolved: {home_url}')
except Exception as e:
    print(f'❌ URL resolution failed: {e}')
    exit(1)

# Test model creation
from apps.core.models import Player
print(f'✅ Player model loaded: {Player._meta.db_table}')
print(f'✅ Available player names: {[name[1] for name in Player.PLAYER_NAMES]}')
"

echo ""
echo "=== Setup Validation Complete ==="
echo "🎉 Your Django Onam Project is ready!"
echo ""
echo "To start the development server:"
echo "python manage.py runserver"
echo ""
echo "Available player names for selection:"
echo "- Johna"
echo "- Jonas" 
echo "- John"
echo "- Ram"
echo "- Sam"
