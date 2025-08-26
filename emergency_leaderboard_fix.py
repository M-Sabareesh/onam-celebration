#!/usr/bin/env python
"""
Emergency Production Database Fix
This script applies the missing individual event models migrations.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

def setup_django():
    """Setup Django environment"""
    # Try different settings modules in order of preference
    settings_modules = [
        'onam_project.settings.base',
        'onam_project.settings.production', 
        'onam_project.settings'
    ]
    
    for settings_module in settings_modules:
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
            django.setup()
            print(f"✅ Django setup successful with {settings_module}")
            return True
        except Exception as e:
            print(f"⚠ Failed to setup with {settings_module}: {e}")
            continue
    
    print("❌ Failed to setup Django with any settings module")
    return False

def check_missing_tables():
    """Check which tables are missing"""
    print("🔍 Checking for missing database tables...")
    
    missing_tables = []
    required_tables = [
        'core_individualeventscore',
        'core_individualparticipation', 
        'core_individualeventvote',
        'core_teameventparticipation'
    ]
    
    with connection.cursor() as cursor:
        for table in required_tables:
            try:
                # Try SQLite syntax first
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name = ?;
                """, [table])
                
                if cursor.fetchone():
                    print(f"  ✅ {table} exists")
                else:
                    print(f"  ❌ {table} MISSING")
                    missing_tables.append(table)
            except Exception:
                try:
                    # Try PostgreSQL/MySQL syntax
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_name = %s;
                    """, [table])
                    
                    if cursor.fetchone():
                        print(f"  ✅ {table} exists")
                    else:
                        print(f"  ❌ {table} MISSING")
                        missing_tables.append(table)
                except Exception as e:
                    print(f"  ⚠ Could not check {table}: {e}")
                    missing_tables.append(table)
    
    return missing_tables

def apply_core_migrations():
    """Apply the core app migrations"""
    print("\n🔄 Applying core app migrations...")
    
    try:
        # Apply migrations in sequence
        migrations = [
            ['migrate', 'core', '0010'],  # Individual event models
            ['migrate', 'core', '0011'],  # Fix individual vote fields
            ['migrate', 'core', '0012'],  # Team event participation
            ['migrate'],  # Apply any remaining migrations
        ]
        
        for migration_cmd in migrations:
            try:
                print(f"Running: python manage.py {' '.join(migration_cmd)}")
                execute_from_command_line(['manage.py'] + migration_cmd)
                print(f"✅ Success: {' '.join(migration_cmd)}")
            except Exception as e:
                print(f"⚠️ Warning for {' '.join(migration_cmd)}: {e}")
                # Continue with other migrations
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_missing_tables_manually():
    """Create missing tables manually if migrations fail"""
    print("\n🛠️ Creating missing tables manually...")
    
    try:
        with connection.cursor() as cursor:
            # Create IndividualEventScore table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_individualeventscore (
                    id BIGSERIAL PRIMARY KEY,
                    event_id BIGINT NOT NULL REFERENCES core_event(id),
                    player_id BIGINT NOT NULL REFERENCES core_player(id),
                    points DECIMAL(5,2) DEFAULT 0,
                    team_points DECIMAL(5,2) DEFAULT 0,
                    notes TEXT DEFAULT '',
                    awarded_by VARCHAR(100) DEFAULT '',
                    awarded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    UNIQUE(event_id, player_id)
                );
            """)
            print("✅ Created core_individualeventscore table")
            
            # Create IndividualParticipation table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_individualparticipation (
                    id BIGSERIAL PRIMARY KEY,
                    event_id BIGINT NOT NULL REFERENCES core_event(id),
                    player_id BIGINT NOT NULL REFERENCES core_player(id),
                    registered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    UNIQUE(event_id, player_id)
                );
            """)
            print("✅ Created core_individualparticipation table")
            
            # Create IndividualEventVote table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_individualeventvote (
                    id BIGSERIAL PRIMARY KEY,
                    event_id BIGINT NOT NULL REFERENCES core_event(id),
                    voting_player_id BIGINT NOT NULL REFERENCES core_player(id),
                    performing_player_id BIGINT NOT NULL REFERENCES core_player(id),
                    skill_score INTEGER,
                    creativity_score INTEGER,
                    presentation_score INTEGER,
                    overall_score INTEGER,
                    comments TEXT DEFAULT '',
                    voted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    UNIQUE(event_id, voting_player_id, performing_player_id)
                );
            """)
            print("✅ Created core_individualeventvote table")
            
            # Create TeamEventParticipation table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_teameventparticipation (
                    id BIGSERIAL PRIMARY KEY,
                    event_score_id BIGINT NOT NULL REFERENCES core_eventscore(id),
                    player_id BIGINT NOT NULL REFERENCES core_player(id),
                    participated BOOLEAN DEFAULT FALSE,
                    notes TEXT DEFAULT '',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    UNIQUE(event_score_id, player_id)
                );
            """)
            print("✅ Created core_teameventparticipation table")
        
        return True
        
    except Exception as e:
        print(f"❌ Manual table creation failed: {e}")
        return False

def mark_migrations_applied():
    """Mark the migrations as applied in django_migrations table"""
    print("\n📝 Marking migrations as applied...")
    
    try:
        with connection.cursor() as cursor:
            migrations_to_mark = [
                ('core', '0010_individual_event_models'),
                ('core', '0011_fix_individual_vote_null_fields'),
                ('core', '0012_team_event_participation'),
            ]
            
            for app, migration in migrations_to_mark:
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES (%s, %s, NOW()) 
                    ON CONFLICT (app, name) DO NOTHING;
                """, [app, migration])
                print(f"✅ Marked {migration} as applied")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to mark migrations: {e}")
        return False

def main():
    """Main function"""
    print("🚨 Emergency Database Fix for Leaderboard")
    print("=" * 50)
    
    # Setup Django
    setup_django()
    
    # Check what's missing
    missing_tables = check_missing_tables()
    
    if not missing_tables:
        print("\n✅ All tables exist! The issue might be elsewhere.")
        return
    
    print(f"\n🔧 Found {len(missing_tables)} missing tables")
    
    # Try applying migrations first
    if apply_core_migrations():
        print("\n✅ Migrations applied successfully!")
    else:
        print("\n⚠️ Migrations failed, trying manual table creation...")
        if create_missing_tables_manually():
            mark_migrations_applied()
            print("\n✅ Manual table creation successful!")
        else:
            print("\n❌ Manual creation also failed")
            return
    
    # Verify fix
    missing_after = check_missing_tables()
    if not missing_after:
        print("\n🎉 SUCCESS! All database tables are now created!")
        print("\n✅ Your leaderboard should now work!")
        print("🔄 Please restart your Django application")
    else:
        print(f"\n⚠️ Still missing {len(missing_after)} tables:")
        for table in missing_after:
            print(f"  - {table}")

if __name__ == '__main__':
    main()
