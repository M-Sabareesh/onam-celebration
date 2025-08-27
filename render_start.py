#!/usr/bin/env python
"""
Smart deployment script for Render - handles database setup gracefully.
Updated to handle missing TeamConfiguration table.
"""

import os
import sys
import django

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onam_project.settings.production")

# Force database sessions instead of cache sessions if Redis fails
os.environ.setdefault("USE_DATABASE_SESSIONS", "True")

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.utils import OperationalError

def check_database_setup():
    """Check if database is accessible and has basic tables."""
    try:
        # Try to access the database
        connection.ensure_connection()
        
        # Check if django_migrations table exists (indicates migrations have been run)
        with connection.cursor() as cursor:
            try:
                # For PostgreSQL
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_name = 'django_migrations'
                    LIMIT 1;
                """)
                result = cursor.fetchone()
                if result:
                    return True
            except:
                pass
            
            try:
                # For SQLite
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='django_migrations'
                    LIMIT 1;
                """)
                result = cursor.fetchone()
                return result is not None
            except:
                return False
                
    except OperationalError:
        return False
    except Exception:
        return False

def ensure_team_configuration_table():
    """Ensure TeamConfiguration table exists and has default data"""
    try:
        print("🏆 Checking TeamConfiguration table...")
        
        with connection.cursor() as cursor:
            # Check if table exists
            try:
                cursor.execute("SELECT COUNT(*) FROM core_teamconfiguration LIMIT 1;")
                count = cursor.fetchone()[0]
                print(f"✅ TeamConfiguration table exists with {count} teams")
                
                # If table exists but is empty, add default teams
                if count == 0:
                    print("📝 Adding default teams...")
                    default_teams = [
                        ('team_1', 'Red Warriors'),
                        ('team_2', 'Blue Champions'),
                        ('team_3', 'Green Masters'),
                        ('team_4', 'Yellow Legends'),
                        ('unassigned', 'Unassigned'),
                    ]
                    
                    for team_code, team_name in default_teams:
                        cursor.execute("""
                            INSERT OR IGNORE INTO core_teamconfiguration 
                            (team_code, team_name, is_active, created_at, updated_at)
                            VALUES (?, ?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """, [team_code, team_name])
                    
                    print("✅ Default teams added")
                
                return True
                
            except OperationalError as e:
                if "no such table" in str(e).lower():
                    print("🛠️  Creating TeamConfiguration table...")
                    
                    # Create the table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS core_teamconfiguration (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            team_code VARCHAR(20) UNIQUE NOT NULL,
                            team_name VARCHAR(100) NOT NULL,
                            is_active BOOLEAN DEFAULT 1,
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    
                    # Add default teams
                    default_teams = [
                        ('team_1', 'Red Warriors'),
                        ('team_2', 'Blue Champions'),
                        ('team_3', 'Green Masters'),
                        ('team_4', 'Yellow Legends'),
                        ('unassigned', 'Unassigned'),
                    ]
                    
                    for team_code, team_name in default_teams:
                        cursor.execute("""
                            INSERT OR IGNORE INTO core_teamconfiguration 
                            (team_code, team_name, is_active, created_at, updated_at)
                            VALUES (?, ?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """, [team_code, team_name])
                    
                    print("✅ TeamConfiguration table created with default teams")
                    return True
                else:
                    raise e
                    
    except Exception as e:
        print(f"⚠️  Could not setup TeamConfiguration: {e}")
        return False
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
    
    # Step 3: Collect static files (required for production)
    try:
        print("Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
        print("✓ Static files collected")
    except SystemExit:
        print("✓ Static files collection completed")
    except Exception as e:
        print(f"⚠ Static files warning: {e}")
    
    # Step 4: Create cache table if using database cache
    try:
        print("Creating database cache table...")
        execute_from_command_line(['manage.py', 'createcachetable'])
        print("✓ Cache table created")
    except SystemExit:
        print("✓ Cache table creation completed")
    except Exception as e:
        print(f"⚠ Cache table warning: {e}")
    
    # Step 5: Start server (always run)
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
