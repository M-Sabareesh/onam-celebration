#!/usr/bin/env python
"""
Emergency migration fix for missing SimpleEventScore table
This script specifically handles the missing core_simpleeventscore table
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def run_command(cmd, description):
    """Run a Django management command"""
    print(f"🔧 {description}...")
    try:
        execute_from_command_line(cmd.split())
        print(f"✅ {description} completed")
        return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_table_exists():
    """Check if the SimpleEventScore table exists"""
    try:
        django.setup()
        from apps.core.models import SimpleEventScore
        # Try to query the model
        count = SimpleEventScore.objects.count()
        print(f"✅ SimpleEventScore table exists with {count} records")
        return True
    except Exception as e:
        print(f"❌ SimpleEventScore table missing: {e}")
        return False

def main():
    """Emergency migration fix"""
    print("🚨 EMERGENCY MIGRATION FIX")
    print("=" * 50)
    print("Issue: core_simpleeventscore table does not exist")
    print("Solution: Apply missing migration 0015_simple_event_scoring")
    print("=" * 50)
    
    # Check current state
    print("\n1️⃣ Checking current table state...")
    table_exists = check_table_exists()
    
    if table_exists:
        print("✅ Table already exists - no fix needed!")
        return 0
    
    # Show migration status
    print("\n2️⃣ Checking migration status...")
    if not run_command("python manage.py showmigrations core", "Show core app migrations"):
        print("⚠️ Could not check migration status, proceeding anyway...")
    
    # Run migrations
    print("\n3️⃣ Applying missing migrations...")
    if not run_command("python manage.py migrate core", "Apply core app migrations"):
        print("❌ Failed to apply core migrations")
        return 1
    
    # Run all migrations as backup
    print("\n4️⃣ Ensuring all migrations are applied...")
    if not run_command("python manage.py migrate", "Apply all pending migrations"):
        print("❌ Failed to apply all migrations")
        return 1
    
    # Verify fix
    print("\n5️⃣ Verifying the fix...")
    if check_table_exists():
        print("\n🎉 SUCCESS! SimpleEventScore table now exists")
        print("✅ You can now access /admin/core/simpleeventscore/")
        return 0
    else:
        print("\n❌ FAILED! Table still missing after migrations")
        return 1

if __name__ == "__main__":
    sys.exit(main())
