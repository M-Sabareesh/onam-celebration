# Emergency Database Fix for Production
# Run this in Django shell or as a management command

import os
import django
from django.db import connection

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
django.setup()

def add_participation_type_column():
    """Add the missing participation_type column directly"""
    with connection.cursor() as cursor:
        try:
            # Check if column exists first
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'core_event' 
                AND column_name = 'participation_type';
            """)
            
            if not cursor.fetchone():
                print("Adding participation_type column...")
                cursor.execute("""
                    ALTER TABLE core_event 
                    ADD COLUMN participation_type VARCHAR(20) DEFAULT 'team';
                """)
                print("✅ participation_type column added")
            else:
                print("✅ participation_type column already exists")
                
        except Exception as e:
            print(f"❌ Error adding participation_type: {e}")

def add_individual_points_multiplier():
    """Add the individual_points_multiplier column"""
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'core_event' 
                AND column_name = 'individual_points_multiplier';
            """)
            
            if not cursor.fetchone():
                print("Adding individual_points_multiplier column...")
                cursor.execute("""
                    ALTER TABLE core_event 
                    ADD COLUMN individual_points_multiplier DECIMAL(5,2) DEFAULT 1.0;
                """)
                print("✅ individual_points_multiplier column added")
            else:
                print("✅ individual_points_multiplier column already exists")
                
        except Exception as e:
            print(f"❌ Error adding individual_points_multiplier: {e}")

def add_eventscore_fields():
    """Add missing EventScore fields"""
    with connection.cursor() as cursor:
        try:
            # Add points_per_participant
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'core_eventscore' 
                AND column_name = 'points_per_participant';
            """)
            
            if not cursor.fetchone():
                print("Adding points_per_participant column...")
                cursor.execute("""
                    ALTER TABLE core_eventscore 
                    ADD COLUMN points_per_participant DECIMAL(5,2) DEFAULT 0;
                """)
                print("✅ points_per_participant column added")
            
            # Add auto_calculate_points
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'core_eventscore' 
                AND column_name = 'auto_calculate_points';
            """)
            
            if not cursor.fetchone():
                print("Adding auto_calculate_points column...")
                cursor.execute("""
                    ALTER TABLE core_eventscore 
                    ADD COLUMN auto_calculate_points BOOLEAN DEFAULT FALSE;
                """)
                print("✅ auto_calculate_points column added")
                
        except Exception as e:
            print(f"❌ Error adding EventScore fields: {e}")

def create_team_participation_table():
    """Create TeamEventParticipation table"""
    with connection.cursor() as cursor:
        try:
            # Check if table exists
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'core_teameventparticipation';
            """)
            
            if not cursor.fetchone():
                print("Creating TeamEventParticipation table...")
                cursor.execute("""
                    CREATE TABLE core_teameventparticipation (
                        id BIGSERIAL PRIMARY KEY,
                        event_score_id BIGINT NOT NULL,
                        player_id BIGINT NOT NULL,
                        participated BOOLEAN DEFAULT FALSE,
                        notes TEXT DEFAULT '',
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        FOREIGN KEY (event_score_id) REFERENCES core_eventscore(id) ON DELETE CASCADE,
                        FOREIGN KEY (player_id) REFERENCES core_player(id) ON DELETE CASCADE,
                        UNIQUE(event_score_id, player_id)
                    );
                """)
                print("✅ TeamEventParticipation table created")
            else:
                print("✅ TeamEventParticipation table already exists")
                
        except Exception as e:
            print(f"❌ Error creating TeamEventParticipation table: {e}")

def create_individual_models():
    """Create individual event models"""
    with connection.cursor() as cursor:
        try:
            # IndividualParticipation table
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'core_individualparticipation';
            """)
            
            if not cursor.fetchone():
                print("Creating IndividualParticipation table...")
                cursor.execute("""
                    CREATE TABLE core_individualparticipation (
                        id BIGSERIAL PRIMARY KEY,
                        event_id BIGINT NOT NULL,
                        player_id BIGINT NOT NULL,
                        registered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        FOREIGN KEY (event_id) REFERENCES core_event(id) ON DELETE CASCADE,
                        FOREIGN KEY (player_id) REFERENCES core_player(id) ON DELETE CASCADE,
                        UNIQUE(event_id, player_id)
                    );
                """)
                print("✅ IndividualParticipation table created")
            
            # IndividualEventScore table
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'core_individualeventScore';
            """)
            
            if not cursor.fetchone():
                print("Creating IndividualEventScore table...")
                cursor.execute("""
                    CREATE TABLE core_individualeventScore (
                        id BIGSERIAL PRIMARY KEY,
                        event_id BIGINT NOT NULL,
                        player_id BIGINT NOT NULL,
                        points DECIMAL(5,2) DEFAULT 0,
                        team_points DECIMAL(5,2) DEFAULT 0,
                        notes TEXT DEFAULT '',
                        awarded_by VARCHAR(100) DEFAULT '',
                        awarded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        FOREIGN KEY (event_id) REFERENCES core_event(id) ON DELETE CASCADE,
                        FOREIGN KEY (player_id) REFERENCES core_player(id) ON DELETE CASCADE,
                        UNIQUE(event_id, player_id)
                    );
                """)
                print("✅ IndividualEventScore table created")
                
        except Exception as e:
            print(f"❌ Error creating individual models: {e}")

def update_migration_history():
    """Update Django migration history"""
    with connection.cursor() as cursor:
        try:
            # Mark migrations as applied
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
                
        except Exception as e:
            print(f"❌ Error updating migration history: {e}")

def main():
    print("🚨 Emergency Database Fix - Running Direct SQL")
    print("=" * 50)
    
    # Add missing columns and tables
    add_participation_type_column()
    add_individual_points_multiplier()
    add_eventscore_fields()
    create_team_participation_table()
    create_individual_models()
    update_migration_history()
    
    print("\n✅ Emergency fix completed!")
    print("🔄 Please restart your Django application")

if __name__ == '__main__':
    main()
