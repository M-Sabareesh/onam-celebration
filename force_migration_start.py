#!/usr/bin/env python3
"""
FORCED MIGRATION RENDER START
This script will force-apply the missing migration before starting
"""

import os
import sys
import subprocess

def main():
    """Force migration and start"""
    print("🚨 FORCED MIGRATION RENDER START")
    print("=" * 50)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
    
    try:
        # FORCE: Check if migration exists
        print("1️⃣ Checking migration 0015...")
        result = subprocess.run([
            'python', 'manage.py', 'showmigrations', 'core'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("Migration status:")
            print(result.stdout)
        
        # FORCE: Apply specific migration
        print("\n2️⃣ FORCING migration 0015...")
        result = subprocess.run([
            'python', 'manage.py', 'migrate', 'core', '0015', '--verbosity=2'
        ], capture_output=True, text=True, timeout=60)
        
        print("Migration output:")
        print(result.stdout)
        if result.stderr:
            print("Migration errors:")
            print(result.stderr)
        
        # FORCE: Run all migrations
        print("\n3️⃣ Running all migrations...")
        subprocess.run([
            'python', 'manage.py', 'migrate', '--noinput'
        ], timeout=60)
        
        # FORCE: Collect static
        print("\n4️⃣ Collecting static files...")
        subprocess.run([
            'python', 'manage.py', 'collectstatic', '--noinput'
        ], timeout=60)
        
        # VERIFY: Check tables
        print("\n5️⃣ Verifying tables...")
        verify_script = '''
from django.db import connection
cursor = connection.cursor()
tables = ["core_simpleeventscore", "core_simpleeventscore_participants"]
for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"✅ {table}: {count} rows")
    except Exception as e:
        print(f"❌ {table}: {e}")
'''
        
        subprocess.run([
            'python', 'manage.py', 'shell', '-c', verify_script
        ], timeout=30)
        
    except Exception as e:
        print(f"Setup error: {e}")
    
    print("\n🚀 STARTING GUNICORN...")
    print("=" * 50)
    
    # Start server
    port = os.environ.get('PORT', '10000')
    workers = os.environ.get('WEB_CONCURRENCY', '1')
    
    os.execvp('gunicorn', [
        'gunicorn',
        'onam_project.wsgi:application',
        '--bind', f'0.0.0.0:{port}',
        '--workers', str(workers),
        '--timeout', '120'
    ])

if __name__ == "__main__":
    main()
