#!/usr/bin/env python
"""
Script to force migration and create Event tables
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

def force_migration():
    """Force migration and create tables"""
    print("=== Forcing Migration for Event Models ===")
    
    try:
        from django.core.management import execute_from_command_line
        from django.db import connection
        
        # Check current migration status
        print("Checking migration status...")
        
        # Apply migrations
        print("Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        
        print("✓ Migrations applied successfully")
        
        # Test if tables exist
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'core_%';")
        tables = cursor.fetchall()
        
        print(f"\nExisting core tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check if our new tables exist
        expected_tables = ['core_event', 'core_eventparticipation', 'core_eventvote']
        for table_name in expected_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            exists = cursor.fetchone()
            if exists:
                print(f"✓ Table {table_name} exists")
            else:
                print(f"✗ Table {table_name} missing")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        
        # Try alternative approach - create tables manually
        print("\nTrying alternative approach...")
        try:
            from django.core.management.color import no_style
            from django.db import connection
            from apps.core.models import Event, EventParticipation, EventVote
            
            style = no_style()
            sql = connection.ops.sql_table_creation_suffix()
            
            # Get SQL statements for creating tables
            from django.core.management.sql import sql_create_index
            from django.db import models
            
            print("Creating tables manually...")
            
            # This is a simplified approach - in practice, use migrations
            cursor = connection.cursor()
            
            # Create Event table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS core_event (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    event_type VARCHAR(20) NOT NULL,
                    description TEXT,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    voting_enabled BOOLEAN NOT NULL DEFAULT 0,
                    created_at DATETIME NOT NULL
                );
            ''')
            
            # Create EventParticipation table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS core_eventparticipation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER NOT NULL,
                    team VARCHAR(20) NOT NULL,
                    registered_at DATETIME NOT NULL,
                    FOREIGN KEY (event_id) REFERENCES core_event (id),
                    UNIQUE(event_id, team)
                );
            ''')
            
            # Create EventVote table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS core_eventvote (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER NOT NULL,
                    voting_team VARCHAR(20) NOT NULL,
                    performing_team VARCHAR(20) NOT NULL,
                    coordination_score INTEGER NOT NULL,
                    selection_score INTEGER NOT NULL,
                    overall_score INTEGER NOT NULL,
                    enjoyment_score INTEGER NOT NULL,
                    comments TEXT,
                    voted_at DATETIME NOT NULL,
                    FOREIGN KEY (event_id) REFERENCES core_event (id),
                    UNIQUE(event_id, voting_team, performing_team)
                );
            ''')
            
            connection.commit()
            print("✓ Tables created manually")
            
        except Exception as e2:
            print(f"Manual table creation also failed: {e2}")
    
    # Test table creation
    try:
        from apps.core.models import Event
        
        # Try to query the Event model
        count = Event.objects.count()
        print(f"✓ Event model working - found {count} events")
        
    except Exception as e:
        print(f"✗ Event model still not working: {e}")

if __name__ == "__main__":
    force_migration()
