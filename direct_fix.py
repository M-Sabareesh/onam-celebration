#!/usr/bin/env python3
"""
Direct Database Fix Script
Fix the database directly using Django ORM
"""
import os
import sys

# Add the project to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')

# Setup Django
import django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection, migrations
from django.core.management.color import no_style
from django.db import models

def run_specific_migrations():
    """Run specific migrations that might be missing"""
    try:
        print("🔧 Running migrations...")
        
        # Run migrations for each app
        apps_to_migrate = ['contenttypes', 'auth', 'sessions', 'admin', 'core', 'accounts', 'games']
        
        for app in apps_to_migrate:
            try:
                execute_from_command_line(['manage.py', 'migrate', app, '--verbosity=2'])
                print(f"✅ {app} migrations applied")
            except Exception as e:
                print(f"⚠️ {app} migration issue: {e}")
        
        # Run all migrations
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        print("✅ All migrations completed")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    
    return True

def verify_teamconfiguration_table():
    """Check if TeamConfiguration table exists and has data"""
    try:
        from apps.core.models import TeamConfiguration
        
        # Try to query the table
        count = TeamConfiguration.objects.count()
        print(f"✅ TeamConfiguration table exists with {count} records")
        
        if count == 0:
            print("📋 Creating default team configurations...")
            teams = [
                {'team_code': 'team_1', 'team_name': 'Team Maveli'},
                {'team_code': 'team_2', 'team_name': 'Team Onam'},
                {'team_code': 'team_3', 'team_name': 'Team Thiruvonam'},
                {'team_code': 'team_4', 'team_name': 'Team Pookalam'}
            ]
            
            for team in teams:
                config, created = TeamConfiguration.objects.get_or_create(
                    team_code=team['team_code'],
                    defaults={'team_name': team['team_name']}
                )
                if created:
                    print(f"   ✅ Created: {team['team_name']}")
                else:
                    print(f"   ✅ Exists: {team['team_name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ TeamConfiguration table error: {e}")
        return False

def check_database_integrity():
    """Check database integrity"""
    try:
        with connection.cursor() as cursor:
            # Check if core_teamconfiguration table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_teamconfiguration';")
            result = cursor.fetchone()
            
            if result:
                print("✅ core_teamconfiguration table exists in database")
                
                # Check table structure
                cursor.execute("PRAGMA table_info(core_teamconfiguration);")
                columns = cursor.fetchall()
                print(f"   📋 Table has {len(columns)} columns:")
                for col in columns:
                    print(f"      - {col[1]} ({col[2]})")
                
                # Check data
                cursor.execute("SELECT COUNT(*) FROM core_teamconfiguration;")
                count = cursor.fetchone()[0]
                print(f"   📊 Table has {count} records")
                
                return True
            else:
                print("❌ core_teamconfiguration table missing from database")
                return False
                
    except Exception as e:
        print(f"❌ Database check error: {e}")
        return False

def main():
    """Main function"""
    print("🚨 DIRECT DATABASE FIX")
    print("=" * 40)
    
    # Step 1: Run migrations
    print("\n1️⃣ Running migrations...")
    migrations_ok = run_specific_migrations()
    
    # Step 2: Check database integrity
    print("\n2️⃣ Checking database integrity...")
    db_ok = check_database_integrity()
    
    # Step 3: Verify TeamConfiguration
    print("\n3️⃣ Verifying TeamConfiguration...")
    team_ok = verify_teamconfiguration_table()
    
    # Summary
    print("\n" + "=" * 40)
    if migrations_ok and db_ok and team_ok:
        print("✅ FIX COMPLETE! Database is ready.")
        print("🌐 You can now run the server:")
        print("   python manage.py runserver")
        print("🏆 Admin panel: http://localhost:8000/admin/")
    else:
        print("❌ Some issues remain. Check the errors above.")
    
    return migrations_ok and db_ok and team_ok

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Fix interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
