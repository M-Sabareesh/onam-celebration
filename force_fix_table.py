#!/usr/bin/env python3
"""
IMMEDIATE FIX for missing core_simpleeventscore table
This script will force create the missing table
"""

import os
import sys
import subprocess
import django

def run_sql_command(sql, description):
    """Run a raw SQL command"""
    print(f"🔧 {description}...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
        django.setup()
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(sql)
        print(f"✅ {description} completed")
        return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def force_create_table():
    """Force create the SimpleEventScore table"""
    print("🚨 FORCE CREATING MISSING TABLE")
    
    # SQL to create the missing table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS core_simpleeventscore (
        id BIGSERIAL PRIMARY KEY,
        team VARCHAR(20) NOT NULL,
        event_type VARCHAR(20) DEFAULT 'team' NOT NULL,
        points DECIMAL(6,2) DEFAULT 0 NOT NULL,
        notes TEXT NOT NULL DEFAULT '',
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        event_id BIGINT NOT NULL
    );
    
    -- Add foreign key constraint
    ALTER TABLE core_simpleeventscore 
    ADD CONSTRAINT core_simpleeventscore_event_id_fkey 
    FOREIGN KEY (event_id) REFERENCES core_event(id) ON DELETE CASCADE;
    
    -- Create participants table
    CREATE TABLE IF NOT EXISTS core_simpleeventscore_participants (
        id BIGSERIAL PRIMARY KEY,
        simpleeventscore_id BIGINT NOT NULL,
        player_id BIGINT NOT NULL,
        UNIQUE(simpleeventscore_id, player_id)
    );
    
    -- Add foreign key constraints for participants
    ALTER TABLE core_simpleeventscore_participants 
    ADD CONSTRAINT core_simpleeventscore_participants_simpleeventscore_id_fkey 
    FOREIGN KEY (simpleeventscore_id) REFERENCES core_simpleeventscore(id) ON DELETE CASCADE;
    
    ALTER TABLE core_simpleeventscore_participants 
    ADD CONSTRAINT core_simpleeventscore_participants_player_id_fkey 
    FOREIGN KEY (player_id) REFERENCES core_player(id) ON DELETE CASCADE;
    
    -- Create indexes
    CREATE INDEX IF NOT EXISTS core_simpleeventscore_event_id_idx ON core_simpleeventscore(event_id);
    CREATE INDEX IF NOT EXISTS core_simpleeventscore_team_idx ON core_simpleeventscore(team);
    """
    
    return run_sql_command(create_table_sql, "Create SimpleEventScore table manually")

def mark_migration_applied():
    """Mark the migration as applied"""
    mark_sql = """
    INSERT INTO django_migrations (app, name, applied) 
    VALUES ('core', '0015_simple_event_scoring', NOW())
    ON CONFLICT (app, name) DO NOTHING;
    """
    
    return run_sql_command(mark_sql, "Mark migration as applied")

def test_table():
    """Test that the table works"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
        django.setup()
        
        from apps.core.models import SimpleEventScore
        count = SimpleEventScore.objects.count()
        print(f"✅ SimpleEventScore table working: {count} records")
        return True
    except Exception as e:
        print(f"❌ Table test failed: {e}")
        return False

def main():
    """Force fix the missing table"""
    print("🚨 IMMEDIATE TABLE FIX")
    print("=" * 40)
    
    # Force create table
    if not force_create_table():
        print("❌ Failed to create table")
        return 1
    
    # Mark migration as applied
    mark_migration_applied()
    
    # Test table
    if test_table():
        print("🎉 SUCCESS! Table is now working")
        return 0
    else:
        print("❌ Table still not working")
        return 1

if __name__ == "__main__":
    sys.exit(main())
