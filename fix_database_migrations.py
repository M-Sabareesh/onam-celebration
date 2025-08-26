#!/usr/bin/env python
"""
Fix Database Migrations Script
This script will handle the database migration issues and static file problems.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
    try:
        django.setup()
    except Exception as e:
        print(f"Django setup error: {e}")
        # Try development settings if production fails
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
        django.setup()

def run_migrations():
    """Run database migrations"""
    print("=== Running Database Migrations ===")
    
    try:
        # Generate any missing migrations
        print("1. Generating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Apply migrations
        print("2. Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Migrations completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    
    return True

def collect_static():
    """Collect static files"""
    print("\n=== Collecting Static Files ===")
    
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected successfully!")
        return True
    except Exception as e:
        print(f"❌ Static files error: {e}")
        return False

def check_database():
    """Check if database tables exist"""
    print("\n=== Checking Database ===")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            # Check if Event table has participation_type column
            cursor.execute("PRAGMA table_info(core_event);")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'participation_type' in columns:
                print("✅ participation_type column exists")
            else:
                print("❌ participation_type column missing")
                return False
                
            # Check if TeamEventParticipation table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_teameventparticipation';")
            if cursor.fetchone():
                print("✅ TeamEventParticipation table exists")
            else:
                print("❌ TeamEventParticipation table missing")
                return False
                
        return True
    except Exception as e:
        print(f"❌ Database check error: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing Database Migrations and Static Files\n")
    
    # Setup Django
    setup_django()
    
    # Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations")
        return
    
    # Check database state
    if not check_database():
        print("❌ Database issues remain")
        return
    
    # Collect static files
    if not collect_static():
        print("⚠️  Static files collection failed, but migrations succeeded")
    
    print("\n🎉 Database fixes completed!")
    print("\nNext steps:")
    print("1. Restart your Django server")
    print("2. Test the team event participation functionality")
    print("3. Check admin interface for EventScore with participant selection")

if __name__ == '__main__':
    main()
