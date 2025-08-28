@echo off
echo "🔧 Fixing missing SimpleEventScore tables..."

cd /d "c:\Users\SMADAMBA\OneDrive - Volvo Cars\Documents\Testing\Test\onam-celebration\onam-celebration"

echo "📁 Current directory: %CD%"

echo "🔄 Activating virtual environment..."
call env\Scripts\activate.bat

echo "� Checking current migration status..."
python manage.py showmigrations core

echo "�🚀 Running Django migrations for core app..."
python manage.py migrate core --verbosity=2

echo "✅ Checking if tables were created..."
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT COUNT(*) FROM core_simpleeventscore'); print('Main table OK'); cursor.execute('SELECT COUNT(*) FROM core_simpleeventscore_participants'); print('Relationship table OK')"

echo "📋 Final migration status..."
python manage.py showmigrations core

echo "✅ Migration fix completed!"
pause
