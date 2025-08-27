@echo off
REM Emergency Production Database Fix Script for Windows
REM Run this script in your production environment to fix the missing django_session table

echo 🚨 EMERGENCY PRODUCTION DATABASE FIX
echo ====================================

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Apply migrations in the correct order
echo 🔧 Applying Django core migrations...
python manage.py migrate contenttypes
python manage.py migrate auth
python manage.py migrate sessions
python manage.py migrate admin

echo 🔧 Applying app migrations...
python manage.py migrate core
python manage.py migrate accounts
python manage.py migrate games

echo 🔧 Applying all remaining migrations...
python manage.py migrate

REM Create superuser
echo 👤 Creating superuser...
python manage.py shell -c "from django.contrib.auth.models import User; import os; username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'OnamAdmin'); email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'); password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123'); User.objects.create_superuser(username=username, email=email, password=password) if not User.objects.filter(username=username).exists() else print(f'Superuser {username} already exists')"

REM Setup team configurations
echo 🏆 Setting up team configurations...
python manage.py shell -c "from apps.core.models import TeamConfiguration; default_teams = [('team_1', 'Team 1'), ('team_2', 'Team 2'), ('team_3', 'Team 3'), ('team_4', 'Team 4'), ('unassigned', 'Unassigned')]; [TeamConfiguration.objects.get_or_create(team_code=team_code, defaults={'team_name': team_name, 'is_active': True}) for team_code, team_name in default_teams]; print('Team configurations ready!')"

REM Collect static files
echo 📦 Collecting static files...
python manage.py collectstatic --noinput

REM Verify database tables
echo 🔍 Verifying database tables...
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\" ORDER BY name;'); tables = [row[0] for row in cursor.fetchall()]; print(f'Found {len(tables)} database tables'); [print(f'  - {table}') for table in tables]; print('✅ django_session table exists' if 'django_session' in tables else '❌ django_session table missing'); print('✅ TeamConfiguration table exists' if 'core_teamconfiguration' in tables else '❌ TeamConfiguration table missing')"

echo ✅ Production database fix complete!
echo 🌐 Your site should now be accessible
