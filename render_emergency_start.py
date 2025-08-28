#!/usr/bin/env python3
"""
Enhanced Render start script with emergency table fixes
Handles missing tables and migration issues automatically
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

# Add project to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Initialize Django
django.setup()

from django.core.management import call_command, execute_from_command_line
from django.db import connection
from django.conf import settings

def log(message, level="INFO"):
    """Enhanced logging with timestamps"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def check_redis():
    """Check Redis availability"""
    try:
        import redis
        r = redis.Redis(host=os.getenv('REDIS_URL', 'localhost'), port=6379, db=0)
        r.ping()
        log("✅ Redis is available")
        return True
    except Exception as e:
        log(f"⚠ Redis unavailable, using database cache and sessions", "WARN")
        return False

def emergency_table_fix():
    """Create missing tables that cause 500 errors"""
    log("🔧 Running emergency table fixes...")
    
    try:
        with connection.cursor() as cursor:
            # Check for missing core_simpleeventscore table
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'core_simpleeventscore'
                );
            """)
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                log("📋 Creating missing core_simpleeventscore table...")
                
                # Create the table
                cursor.execute("""
                    CREATE TABLE core_simpleeventscore (
                        id SERIAL PRIMARY KEY,
                        event_id INTEGER NOT NULL,
                        team VARCHAR(20) NOT NULL,
                        points INTEGER NOT NULL,
                        notes TEXT,
                        awarded_by VARCHAR(150),
                        awarded_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        CONSTRAINT core_simpleeventscore_event_id_fkey 
                            FOREIGN KEY (event_id) REFERENCES core_event(id) 
                            ON DELETE CASCADE
                    );
                """)
                
                # Create indexes
                cursor.execute("CREATE INDEX core_simpleeventscore_event_id_idx ON core_simpleeventscore(event_id);")
                cursor.execute("CREATE INDEX core_simpleeventscore_team_idx ON core_simpleeventscore(team);")
                cursor.execute("CREATE INDEX core_simpleeventscore_awarded_at_idx ON core_simpleeventscore(awarded_at);")
                
                log("✅ Missing table created successfully!")
            else:
                log("ℹ️ All required tables exist")
                
    except Exception as e:
        log(f"⚠️ Emergency table fix failed: {e}", "ERROR")
        # Continue anyway - migrations might fix it

def run_migrations():
    """Run Django migrations with error handling"""
    log("🔄 Running database migrations...")
    
    try:
        # Try with fake-initial first
        call_command('migrate', '--fake-initial', verbosity=0)
        log("✅ Migrations completed successfully")
        return True
    except Exception as e:
        log(f"⚠️ Fake-initial migration failed: {e}", "WARN")
        
        try:
            # Try without fake-initial
            call_command('migrate', verbosity=0)
            log("✅ Migrations completed (second attempt)")
            return True
        except Exception as e2:
            log(f"❌ All migration attempts failed: {e2}", "ERROR")
            return False

def collect_static_files():
    """Collect static files with error handling"""
    log("📦 Collecting static files...")
    
    try:
        call_command('collectstatic', '--noinput', '--clear', verbosity=0)
        log("✅ Static files collected successfully")
        return True
    except Exception as e:
        log(f"⚠️ Static file collection failed: {e}", "WARN")
        
        try:
            # Try without clear
            call_command('collectstatic', '--noinput', verbosity=0)
            log("✅ Static files collected (without clear)")
            return True
        except Exception as e2:
            log(f"❌ Static file collection failed: {e2}", "ERROR")
            return False

def start_gunicorn():
    """Start Gunicorn server"""
    log("🚀 Starting Gunicorn server...")
    
    # Gunicorn configuration
    bind_address = f"0.0.0.0:{os.getenv('PORT', '10000')}"
    workers = os.getenv('WEB_CONCURRENCY', '2')
    
    gunicorn_cmd = [
        'gunicorn',
        'onam_project.wsgi:application',
        '--bind', bind_address,
        '--workers', str(workers),
        '--worker-class', 'sync',
        '--worker-connections', '1000',
        '--max-requests', '1000',
        '--max-requests-jitter', '100',
        '--timeout', '30',
        '--keep-alive', '5',
        '--log-level', 'info',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--capture-output'
    ]
    
    log(f"📍 Starting server on {bind_address} with {workers} workers")
    
    try:
        subprocess.run(gunicorn_cmd, check=True)
    except subprocess.CalledProcessError as e:
        log(f"💥 Gunicorn failed to start: {e}", "ERROR")
        sys.exit(1)
    except KeyboardInterrupt:
        log("⛔ Server stopped by user")
        sys.exit(0)

def main():
    """Main startup sequence"""
    log("🚀 Enhanced Render Startup with Emergency Fixes")
    log("=" * 50)
    
    # Step 1: Check Redis
    redis_available = check_redis()
    
    # Step 2: Emergency table fixes
    emergency_table_fix()
    
    # Step 3: Run migrations
    migrations_success = run_migrations()
    
    # Step 4: Collect static files
    static_success = collect_static_files()
    
    # Step 5: Log startup status
    log("📊 Startup Status Summary:")
    log(f"   Redis: {'✅ Available' if redis_available else '⚠️ Fallback to DB'}")
    log(f"   Migrations: {'✅ Success' if migrations_success else '❌ Failed'}")
    log(f"   Static Files: {'✅ Success' if static_success else '❌ Failed'}")
    
    if not migrations_success:
        log("⚠️ Starting with migration issues - some features may not work", "WARN")
    
    # Step 6: Start the server
    start_gunicorn()

if __name__ == '__main__':
    main()
