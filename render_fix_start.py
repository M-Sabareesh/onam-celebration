#!/usr/bin/env python3
"""
EMERGENCY RENDER START COMMAND
Fixes missing tables and starts the application
"""

import os
import sys
import subprocess
import time

def run_command(cmd, description, critical=False):
    """Run a command with error handling"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
        else:
            print(f"⚠️  {description} returned code {result.returncode}")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            if critical:
                print(f"❌ Critical step failed, but continuing...")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        if critical:
            print("❌ Critical failure, but continuing...")
        return False

def check_redis():
    """Check if Redis is available"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        return True
    except:
        return False

def main():
    """Emergency startup for Render with table fixes"""
    print("🚨 EMERGENCY RENDER START - FIX MISSING TABLES")
    print("=" * 60)
    
    # Check Redis
    if check_redis():
        print("✅ Redis available")
    else:
        print("⚠️ Redis unavailable, using database cache and sessions")
    
    # STEP 1: Emergency table fix
    print("\n1️⃣ EMERGENCY: Creating missing tables...")
    
    # Try to run the specific migration
    run_command(
        "python manage.py migrate core 0015 --verbosity=1", 
        "Apply SimpleEventScore migration",
        critical=True
    )
    
    # STEP 2: Run all migrations
    print("\n2️⃣ Running all migrations...")
    run_command("python manage.py migrate --noinput", "Complete migration")
    
    # STEP 3: Collect static files
    print("\n3️⃣ Collecting static files...")
    run_command("python manage.py collectstatic --noinput", "Static file collection")
    
    # STEP 4: Create media directories
    print("\n4️⃣ Creating media directories...")
    os.makedirs("media/question_images", exist_ok=True)
    os.makedirs("media/avatars", exist_ok=True)
    os.makedirs("media/treasure_hunt_photos", exist_ok=True)
    print("✅ Media directories created")
    
    # STEP 5: Quick table verification
    print("\n5️⃣ Verifying critical tables exist...")
    verification_cmd = """
from django.db import connection
cursor = connection.cursor()
try:
    cursor.execute('SELECT COUNT(*) FROM core_simpleeventscore')
    print('✅ core_simpleeventscore table exists')
except Exception as e:
    print(f'❌ core_simpleeventscore missing: {e}')
try:
    cursor.execute('SELECT COUNT(*) FROM core_simpleeventscore_participants')
    print('✅ core_simpleeventscore_participants table exists')
except Exception as e:
    print(f'❌ core_simpleeventscore_participants missing: {e}')
"""
    
    run_command(f'python manage.py shell -c "{verification_cmd}"', "Table verification")
    
    print("\n" + "=" * 60)
    print("🚀 STARTING GUNICORN SERVER...")
    print("=" * 60)
    
    # Start the server
    port = os.environ.get('PORT', '10000')
    workers = os.environ.get('WEB_CONCURRENCY', '1')
    
    gunicorn_cmd = f"gunicorn onam_project.wsgi:application --bind 0.0.0.0:{port} --workers {workers} --worker-class sync --timeout 120 --max-requests 1000 --max-requests-jitter 100"
    
    print(f"🌐 Starting server on port {port} with {workers} workers")
    
    # Execute gunicorn
    os.execvp("gunicorn", gunicorn_cmd.split())

if __name__ == "__main__":
    main()
