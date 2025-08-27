#!/bin/bash
# Emergency Production Database Fix Script
# Run this script in your production environment to fix the missing django_session table

echo "🚨 EMERGENCY PRODUCTION DATABASE FIX"
echo "===================================="

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Apply migrations in the correct order
echo "🔧 Applying Django core migrations..."
python manage.py migrate contenttypes
python manage.py migrate auth
python manage.py migrate sessions
python manage.py migrate admin

echo "🔧 Applying app migrations..."
python manage.py migrate core
python manage.py migrate accounts
python manage.py migrate games

echo "🔧 Applying all remaining migrations..."
python manage.py migrate

# Create superuser if environment variables are set
if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Creating superuser..."
    python manage.py shell -c "
from django.contrib.auth.models import User
import os
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'OnamAdmin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists')
"
fi

# Setup team configurations
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

for team_code, team_name in default_teams:
    team, created = TeamConfiguration.objects.get_or_create(
        team_code=team_code,
        defaults={'team_name': team_name, 'is_active': True}
    )
    status = 'Created' if created else 'Updated'
    print(f'{status}: {team.team_code} -> {team.team_name}')

print('Team configurations ready!')
"

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Verify database tables
echo "🔍 Verifying database tables..."
python manage.py shell -c "
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;\")
    tables = [row[0] for row in cursor.fetchall()]

print(f'Found {len(tables)} database tables:')
for table in tables:
    print(f'  - {table}')

if 'django_session' in tables:
    print('✅ django_session table exists')
else:
    print('❌ django_session table missing')

if 'core_teamconfiguration' in tables:
    print('✅ TeamConfiguration table exists')
else:
    print('❌ TeamConfiguration table missing')
"

echo "✅ Production database fix complete!"
echo "🌐 Your site should now be accessible"
