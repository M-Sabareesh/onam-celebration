#!/usr/bin/env python
"""
Create missing SimpleEventScore table manually if migration fails
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def create_table_manually():
    """Create the SimpleEventScore table manually using SQL"""
    print("🔧 Creating SimpleEventScore table manually...")
    
    sql = """
    CREATE TABLE IF NOT EXISTS core_simpleeventscore (
        id BIGSERIAL PRIMARY KEY,
        team VARCHAR(20) NOT NULL,
        event_type VARCHAR(20) DEFAULT 'team' NOT NULL,
        points DECIMAL(6,2) DEFAULT 0 NOT NULL,
        notes TEXT DEFAULT '' NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
        event_id BIGINT NOT NULL REFERENCES core_event(id) ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS core_simpleeventscore_participants (
        id BIGSERIAL PRIMARY KEY,
        simpleeventscore_id BIGINT NOT NULL REFERENCES core_simpleeventscore(id) ON DELETE CASCADE,
        player_id BIGINT NOT NULL REFERENCES core_player(id) ON DELETE CASCADE,
        UNIQUE(simpleeventscore_id, player_id)
    );
    
    CREATE INDEX IF NOT EXISTS core_simpleeventscore_event_id_idx ON core_simpleeventscore(event_id);
    CREATE INDEX IF NOT EXISTS core_simpleeventscore_team_idx ON core_simpleeventscore(team);
    CREATE INDEX IF NOT EXISTS core_simpleeventscore_created_at_idx ON core_simpleeventscore(created_at);
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        print("✅ SimpleEventScore table created manually")
        return True
    except Exception as e:
        print(f"❌ Failed to create table manually: {e}")
        return False

def mark_migration_as_applied():
    """Mark the migration as applied in django_migrations table"""
    print("🔧 Marking migration 0015_simple_event_scoring as applied...")
    
    sql = """
    INSERT INTO django_migrations (app, name, applied) 
    VALUES ('core', '0015_simple_event_scoring', NOW())
    ON CONFLICT (app, name) DO NOTHING;
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        print("✅ Migration marked as applied")
        return True
    except Exception as e:
        print(f"❌ Failed to mark migration: {e}")
        return False

def main():
    """Manual table creation"""
    print("🛠️ MANUAL TABLE CREATION")
    print("=" * 40)
    
    # Create table manually
    if not create_table_manually():
        return 1
    
    # Mark migration as applied
    if not mark_migration_as_applied():
        print("⚠️ Table created but migration not marked - this is OK")
    
    # Test the table
    try:
        from apps.core.models import SimpleEventScore
        count = SimpleEventScore.objects.count()
        print(f"✅ Table working: {count} records found")
        print("🎉 SUCCESS! SimpleEventScore is now ready")
        return 0
    except Exception as e:
        print(f"❌ Table test failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
