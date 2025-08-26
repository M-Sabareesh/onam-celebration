#!/usr/bin/env python
"""
Production Migration Script - Apply all missing migrations to fix database issues
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def check_django_setup():
    """Check if Django is properly configured"""
    try:
        django.setup()
        return True
    except Exception as e:
        print(f"Django setup error: {e}")
        return False

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?;
            """, [table_name])
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        print(f"Error checking table {table_name}: {e}")
        return False

def run_migrations():
    """Apply all missing migrations"""
    print("=== Production Migration Fix ===")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
    
    if not check_django_setup():
        print("Failed to setup Django. Exiting.")
        return False
    
    print("✓ Django setup complete")
    
    # Check current state
    tables_to_check = [
        'core_individualparticipation',
        'core_individualeventscore', 
        'core_individualeventvote',
        'core_teameventparticipation'
    ]
    
    print("\n=== Checking Database Tables ===")
    missing_tables = []
    for table in tables_to_check:
        exists = check_table_exists(table)
        status = "✓ EXISTS" if exists else "✗ MISSING"
        print(f"{table}: {status}")
        if not exists:
            missing_tables.append(table)
    
    if not missing_tables:
        print("\n✓ All required tables exist!")
        return True
    
    print(f"\n⚠ Missing tables: {len(missing_tables)}")
    print("Applying migrations...")
    
    try:
        # Show current migration status
        print("\n=== Current Migration Status ===")
        execute_from_command_line(['manage.py', 'showmigrations', 'core'])
        
        # Apply specific migrations in order
        migrations_to_apply = [
            ['manage.py', 'migrate', 'core', '0010'],
            ['manage.py', 'migrate', 'core', '0011'], 
            ['manage.py', 'migrate', 'core', '0012'],
            ['manage.py', 'migrate']  # Apply any remaining
        ]
        
        for migration_cmd in migrations_to_apply:
            print(f"\n>>> Running: {' '.join(migration_cmd)}")
            try:
                execute_from_command_line(migration_cmd)
                print("✓ Success")
            except Exception as e:
                print(f"⚠ Warning: {e}")
                # Continue with next migration
        
        # Final check
        print("\n=== Final Verification ===")
        all_exist = True
        for table in tables_to_check:
            exists = check_table_exists(table)
            status = "✓ EXISTS" if exists else "✗ STILL MISSING"
            print(f"{table}: {status}")
            if not exists:
                all_exist = False
        
        if all_exist:
            print("\n🎉 All migrations applied successfully!")
            print("The leaderboard should now work properly.")
            return True
        else:
            print("\n⚠ Some tables are still missing. Manual intervention may be required.")
            return False
            
    except Exception as e:
        print(f"Error during migration: {e}")
        return False

def test_leaderboard():
    """Test if leaderboard functionality works"""
    try:
        from apps.core.models import IndividualEventScore, TeamEventParticipation
        from apps.core.views import leaderboard
        print("\n=== Testing Leaderboard Functionality ===")
        
        # Try to import and access the models
        print("✓ IndividualEventScore model accessible")
        print("✓ TeamEventParticipation model accessible")
        
        # Test basic queries
        count = IndividualEventScore.objects.count()
        print(f"✓ IndividualEventScore records: {count}")
        
        return True
    except Exception as e:
        print(f"⚠ Leaderboard test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_migrations()
    
    if success:
        test_leaderboard()
        print("\n✅ Production migration complete!")
        print("You can now restart your Django server.")
    else:
        print("\n❌ Migration failed. Check the errors above.")
        sys.exit(1)
