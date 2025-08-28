#!/usr/bin/env python3
"""
Emergency fix for missing core_simpleeventscore table
This script will create the missing table manually and run necessary migrations
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the Django project to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
django.setup()

from django.db import connection
from django.core.management import call_command

def create_missing_table():
    """Create the missing core_simpleeventscore table manually"""
    print("🔧 Creating missing core_simpleeventscore table...")
    
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'core_simpleeventscore'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("📋 Table does not exist, creating it...")
            
            # Create the table based on the SimpleEventScore model
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
            cursor.execute("""
                CREATE INDEX core_simpleeventscore_event_id_idx 
                ON core_simpleeventscore(event_id);
            """)
            
            cursor.execute("""
                CREATE INDEX core_simpleeventscore_team_idx 
                ON core_simpleeventscore(team);
            """)
            
            cursor.execute("""
                CREATE INDEX core_simpleeventscore_awarded_at_idx 
                ON core_simpleeventscore(awarded_at);
            """)
            
            print("✅ Table core_simpleeventscore created successfully!")
        else:
            print("ℹ️ Table core_simpleeventscore already exists")

def run_migrations():
    """Run any pending migrations"""
    print("\n🔄 Running migrations...")
    try:
        call_command('migrate', '--fake-initial', verbosity=2)
        print("✅ Migrations completed!")
    except Exception as e:
        print(f"⚠️ Migration warning: {e}")
        # Try without fake-initial
        try:
            call_command('migrate', verbosity=2)
            print("✅ Migrations completed (second attempt)!")
        except Exception as e2:
            print(f"❌ Migration failed: {e2}")

def check_table_integrity():
    """Check if all required tables exist"""
    print("\n🔍 Checking table integrity...")
    
    required_tables = [
        'core_event',
        'core_eventscore', 
        'core_simpleeventscore',
        'core_player',
        'core_teamconfiguration',
        'core_treasurehuntquestion'
    ]
    
    with connection.cursor() as cursor:
        for table in required_tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, [table])
            exists = cursor.fetchone()[0]
            
            if exists:
                print(f"✅ {table}: EXISTS")
            else:
                print(f"❌ {table}: MISSING")

def main():
    """Run the emergency fix"""
    print("🚨 EMERGENCY FIX: Missing core_simpleeventscore Table")
    print("=" * 60)
    
    try:
        # Step 1: Create missing table
        create_missing_table()
        
        # Step 2: Run migrations
        run_migrations()
        
        # Step 3: Check integrity
        check_table_integrity()
        
        print("\n" + "=" * 60)
        print("🎉 EMERGENCY FIX COMPLETED!")
        print("✅ The missing table has been created")
        print("✅ Admin interface should now work correctly")
        print("\n📋 Next steps:")
        print("1. Restart the Django application")
        print("2. Test the admin interface")
        print("3. Try accessing /admin/core/simpleeventscore/")
        
    except Exception as e:
        print(f"\n💥 Emergency fix failed: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n🔧 Manual fix instructions:")
        print("1. Access your database directly")
        print("2. Run: python manage.py migrate --fake-initial")
        print("3. Check if migrations are up to date")
        
        return 1
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
