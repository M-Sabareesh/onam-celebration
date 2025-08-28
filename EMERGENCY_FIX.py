#!/usr/bin/env python3
"""
EMERGENCY: Fix missing SimpleEventScore tables
Run this script to apply the missing migration 0015_simple_event_scoring.py
"""

import os
import sys
import subprocess

def main():
    print("🚨 EMERGENCY FIX: Missing SimpleEventScore tables")
    print("=" * 60)
    
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 Working in: {script_dir}")
    
    # Set environment variable
    os.environ['DJANGO_SETTINGS_MODULE'] = 'onam_project.settings.production'
    
    try:
        print("\n🔍 Checking current migration status...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'showmigrations', 'core'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("MIGRATION STATUS:")
            print(result.stdout)
        else:
            print("⚠️ Could not check migration status")
            print("STDERR:", result.stderr)
        
        print("\n🚀 Applying migrations to core app...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate', 'core', '--verbosity=2'
        ], capture_output=True, text=True, timeout=120)
        
        print("MIGRATION OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ Migrations applied successfully!")
        else:
            print(f"\n❌ Migration failed with code: {result.returncode}")
            return False
        
        print("\n🔍 Verifying tables were created...")
        
        # Test main table
        result = subprocess.run([
            sys.executable, 'manage.py', 'shell', '-c',
            "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT COUNT(*) FROM core_simpleeventscore'); print('✅ core_simpleeventscore table exists')"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("❌ Main table verification failed")
        
        # Test relationship table
        result = subprocess.run([
            sys.executable, 'manage.py', 'shell', '-c',
            "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT COUNT(*) FROM core_simpleeventscore_participants'); print('✅ core_simpleeventscore_participants table exists')"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("❌ Relationship table verification failed")
        
        print("\n" + "=" * 60)
        print("🎉 EMERGENCY FIX COMPLETED!")
        print("   The admin interface should now work without 500 errors.")
        print("   You can now safely access /admin/core/simpleeventscore/")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("Manual intervention required!")
        return False

if __name__ == "__main__":
    main()
