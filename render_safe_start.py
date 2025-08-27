#!/usr/bin/env python3
"""
Fixed Start Script for Render Deployment
Only runs team setup if the database is ready, otherwise starts the server
"""

import os
import sys
import django
import subprocess

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def check_database_ready():
    """Check if database has the required tables"""
    try:
        django.setup()
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Check if basic Django tables exist
            cursor.execute("SELECT 1 FROM django_session LIMIT 1;")
            
        print("✅ Database basic tables exist")
        return True
        
    except Exception as e:
        print(f"❌ Database not ready: {e}")
        return False

def check_team_tables():
    """Check if team configuration tables exist"""
    try:
        from apps.core.models import TeamConfiguration
        
        # Try to access the table
        count = TeamConfiguration.objects.count()
        print(f"✅ TeamConfiguration table exists with {count} teams")
        return True
        
    except Exception as e:
        print(f"⚠️  TeamConfiguration table missing: {e}")
        return False

def create_team_table_only():
    """Create only the team configuration table"""
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            print("🛠️  Creating core_teamconfiguration table...")
            
            # Check if table already exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='core_teamconfiguration';
            """)
            
            if cursor.fetchone():
                print("✅ Table already exists")
                return True
            
            # Create the table
            cursor.execute("""
                CREATE TABLE core_teamconfiguration (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_code VARCHAR(20) UNIQUE NOT NULL,
                    team_name VARCHAR(100) NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Insert default teams
            teams = [
                ('team_1', 'Red Warriors'),
                ('team_2', 'Blue Champions'),
                ('team_3', 'Green Masters'),
                ('team_4', 'Yellow Legends'),
                ('unassigned', 'Unassigned'),
            ]
            
            for team_code, team_name in teams:
                cursor.execute("""
                    INSERT OR IGNORE INTO core_teamconfiguration 
                    (team_code, team_name, is_active, created_at, updated_at)
                    VALUES (?, ?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """, [team_code, team_name])
            
            print("✅ TeamConfiguration table created with default teams")
            return True
            
    except Exception as e:
        print(f"❌ Error creating team table: {e}")
        return False

def start_server():
    """Start the Gunicorn server"""
    print("🚀 Starting production server...")
    
    # Get port from environment
    port = os.environ.get('PORT', '8000')
    
    # Start Gunicorn with better error handling
    cmd = [
        'gunicorn',
        'onam_project.wsgi:application',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '1',  # Reduced workers for stability
        '--timeout', '60',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--log-level', 'info'
    ]
    
    try:
        print(f"📡 Server command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("🎉 ONAM CELEBRATION - SAFE STARTUP")
    print("=" * 45)
    
    # Check if database is ready
    if not check_database_ready():
        print("❌ Database not ready, cannot start")
        sys.exit(1)
    
    # Check if team tables exist, create if missing
    if not check_team_tables():
        print("🛠️  Team tables missing, creating them...")
        if not create_team_table_only():
            print("⚠️  Could not create team tables, but continuing...")
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
