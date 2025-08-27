#!/usr/bin/env python3
"""
Emergency Production Database Fix
Fix missing django_session table and ensure all migrations are applied
"""

import os
import sys
import django
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

try:
    django.setup()
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    print("Trying with development settings...")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'onam_project.settings.development'
    django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def check_database_connection():
    """Check if database is accessible"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def list_existing_tables():
    """List all existing tables in the database"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name;
            """)
            tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📋 Found {len(tables)} existing tables:")
        for table in tables:
            print(f"   - {table}")
        return tables
    except Exception as e:
        print(f"❌ Error listing tables: {e}")
        return []

def check_migrations_status():
    """Check which migrations have been applied"""
    try:
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        applied = executor.loader.applied_migrations
        print(f"📊 Applied migrations: {len(applied)}")
        
        # Check for unapplied migrations
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            print(f"⚠️  Unapplied migrations: {len(plan)}")
            for migration, backwards in plan:
                print(f"   - {migration}")
        else:
            print("✅ All migrations are applied")
        
        return len(plan) == 0
    except Exception as e:
        print(f"❌ Error checking migrations: {e}")
        return False

def apply_migrations():
    """Apply all pending migrations"""
    print("🔧 Applying migrations...")
    try:
        # Apply core Django migrations first
        execute_from_command_line(['manage.py', 'migrate', 'contenttypes'])
        execute_from_command_line(['manage.py', 'migrate', 'auth'])
        execute_from_command_line(['manage.py', 'migrate', 'sessions'])
        execute_from_command_line(['manage.py', 'migrate', 'admin'])
        
        # Apply our app migrations
        execute_from_command_line(['manage.py', 'migrate', 'core'])
        execute_from_command_line(['manage.py', 'migrate', 'accounts'])
        execute_from_command_line(['manage.py', 'migrate', 'games'])
        
        # Apply all remaining migrations
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ All migrations applied successfully")
        return True
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
        return False

def create_superuser():
    """Create superuser if it doesn't exist"""
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Creating superuser...")
            User.objects.create_superuser(
                username='OnamAdmin',
                email='mn.sabareesh@gmail.com',
                password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
            )
            print("✅ Superuser created")
        else:
            print("✅ Superuser already exists")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

def setup_team_configurations():
    """Setup default team configurations"""
    try:
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
        
        print(f"✅ Team configurations ready ({created_count} created)")
    except Exception as e:
        print(f"❌ Error setting up teams: {e}")

def collect_static_files():
    """Collect static files for production"""
    try:
        print("📦 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected")
    except Exception as e:
        print(f"❌ Error collecting static files: {e}")

def main():
    """Main fix function"""
    print("🚨 EMERGENCY PRODUCTION DATABASE FIX")
    print("=" * 50)
    
    # Check current environment
    print(f"🔧 Django settings: {settings.SETTINGS_MODULE}")
    print(f"🔧 Database: {settings.DATABASES['default']['ENGINE']}")
    
    # 1. Check database connection
    if not check_database_connection():
        print("❌ Cannot proceed without database connection")
        return False
    
    # 2. List existing tables
    existing_tables = list_existing_tables()
    
    # 3. Check if django_session table exists
    if 'django_session' not in existing_tables:
        print("⚠️  django_session table missing - applying migrations")
    
    # 4. Check migration status
    all_applied = check_migrations_status()
    
    # 5. Apply migrations if needed
    if not all_applied or 'django_session' not in existing_tables:
        if not apply_migrations():
            return False
    
    # 6. Create superuser
    create_superuser()
    
    # 7. Setup team configurations
    setup_team_configurations()
    
    # 8. Collect static files
    collect_static_files()
    
    # 9. Final verification
    print("\n🔍 Final verification...")
    if check_database_connection():
        final_tables = list_existing_tables()
        if 'django_session' in final_tables:
            print("✅ django_session table now exists")
        else:
            print("❌ django_session table still missing")
    
    print("\n✅ Production database fix complete!")
    print("🌐 Your site should now be accessible")
    return True

if __name__ == "__main__":
    main()
