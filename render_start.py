#!/usr/bin/env python
"""
Smart deployment script for Render - only runs migrations and creates superuser when needed.
Based on: python manage.py migrate && python manage.py createsuperuser --noinput || true && python manage.py runserver 0.0.0.0:$PORT
"""

import os
import sys
import django

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onam_project.settings.production")

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.utils import OperationalError

def check_database_setup():
    """Check if database is accessible and has tables."""
    try:
        # Try to access the database
        connection.ensure_connection()
        
        # Check if django_migrations table exists (indicates migrations have been run)
        with connection.cursor() as cursor:
            # Works for both PostgreSQL and SQLite
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_name = 'django_migrations'
                UNION ALL
                SELECT name as table_name FROM sqlite_master 
                WHERE type='table' AND name='django_migrations'
                LIMIT 1;
            """)
            result = cursor.fetchone()
            
        return result is not None
    except OperationalError:
        return False
    except Exception:
        # If the query fails (e.g., information_schema doesn't exist), 
        # try a simpler approach
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM django_migrations LIMIT 1;")
            return True
        except:
            return False

def check_superuser_exists():
    """Check if any superuser exists in the database."""
    try:
        User = get_user_model()
        return User.objects.filter(is_superuser=True).exists()
    except Exception:
        return False

def main():
    print("🚀 Starting Onam Celebration App...")
    
    # Check if database is already set up
    db_setup = check_database_setup()
    
    # Step 1: Run migrations only if database is not set up
    if not db_setup:
        try:
            print("Database not set up. Running migrations...")
            execute_from_command_line(['manage.py', 'migrate'])
            print("✓ Migrations completed")
        except SystemExit:
            print("✓ Migrations completed")
        except Exception as e:
            print(f"✗ Migration failed: {e}")
            sys.exit(1)
    else:
        print("✓ Database already set up, skipping migrations")
    
    # Step 2: Create superuser only if none exists
    if not check_superuser_exists():
        try:
            print("No superuser found. Creating superuser...")
            execute_from_command_line(['manage.py', 'createsuperuser', '--noinput'])
            print("✓ Superuser created")
        except SystemExit:
            print("✓ Superuser creation completed")
        except Exception as e:
            print(f"⚠ Superuser creation warning: {e}")
    else:
        print("✓ Superuser already exists, skipping creation")
    
    # Step 3: Start server (always run)
    port = os.environ.get("PORT", "8000")
    print(f"Starting server on 0.0.0.0:{port}...")
    
    try:
        execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
    except Exception as e:
        print(f"✗ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
