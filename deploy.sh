#!/bin/bash
# Production deployment script for Render
# This script handles database migrations and static files

echo "🚀 Starting Onam Celebration deployment..."

# Set environment
export DJANGO_SETTINGS_MODULE=onam_project.settings.production

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Apply database migrations in correct order
echo "🗄️  Applying database migrations..."
echo "   📋 Applying core Django migrations..."
python manage.py migrate contenttypes --noinput
python manage.py migrate auth --noinput
python manage.py migrate sessions --noinput
python manage.py migrate admin --noinput

echo "   🎯 Applying app migrations..."
python manage.py migrate core --noinput
python manage.py migrate accounts --noinput 2>/dev/null || true
python manage.py migrate games --noinput 2>/dev/null || true

echo "   🔄 Applying all remaining migrations..."
python manage.py migrate --noinput

# Create database cache table
echo "💾 Creating cache table..."
python manage.py createcachetable

# Collect static files (clear old ones first)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create placeholder Maveli images if they don't exist
echo "🖼️  Setting up Maveli images..."
mkdir -p staticfiles/images

# Copy Maveli images from media to static if they exist
if [ -f "media/Maveli/Maveli.jpg" ]; then
    cp media/Maveli/*.jpg staticfiles/images/ 2>/dev/null || true
    cp media/Maveli/*.png staticfiles/images/ 2>/dev/null || true
    echo "✅ Copied Maveli images from media to static"
else
    # Create placeholder files if media images don't exist
    touch staticfiles/images/Maveli.jpg
    touch staticfiles/images/Maveli2.jpg
    touch staticfiles/images/Maveli2.png
    touch staticfiles/images/Maveli4.jpg
    echo "📝 Created Maveli image placeholders"
fi

# Also copy to static directory for local development
mkdir -p static/images
if [ -f "media/Maveli/Maveli.jpg" ]; then
    cp media/Maveli/*.jpg static/images/ 2>/dev/null || true
    cp media/Maveli/*.png static/images/ 2>/dev/null || true
    echo "✅ Copied Maveli images to static/images for development"
fi

# Setup team configurations for admin management
echo "🏆 Setting up team configurations..."
python manage.py shell -c "
from apps.core.models import TeamConfiguration

default_teams = [
    ('team_1', 'Team 1'),
    ('team_2', 'Team 2'),
    ('team_3', 'Team 3'),
    ('team_4', 'Team 4'),
    ('unassigned', 'Unassigned'),
]

created_count = 0
for team_code, team_name in default_teams:
    team, created = TeamConfiguration.objects.get_or_create(
        team_code=team_code,
        defaults={'team_name': team_name, 'is_active': True}
    )
    if created:
        created_count += 1

print(f'Team configurations ready ({created_count} new teams created)')
" 2>/dev/null || echo "   ⚠️  Team configuration setup skipped (will be available after first migration)"

# Create superuser if environment variables are set
if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Creating superuser..."
    python manage.py shell -c "
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'OnamAdmin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists or password not set')
" 2>/dev/null || echo "   ⚠️  Superuser creation skipped"
fi

echo "✅ Deployment completed successfully!"
echo "🎉 Onam celebration website is ready!"
