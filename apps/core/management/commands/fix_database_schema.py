"""
Django Management Command to Fix Database Issues
Usage: python manage.py fix_database_schema
"""

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix missing database columns and tables for team participation system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write("🔍 DRY RUN MODE - No changes will be made")
        
        self.stdout.write("🔧 Fixing database schema for team participation system")
        
        fixes_applied = 0
        
        # Fix 1: Add participation_type column to Event
        if self.add_participation_type_column(dry_run):
            fixes_applied += 1
            
        # Fix 2: Add individual_points_multiplier to Event  
        if self.add_individual_points_multiplier(dry_run):
            fixes_applied += 1
            
        # Fix 3: Add EventScore fields
        if self.add_eventscore_fields(dry_run):
            fixes_applied += 1
            
        # Fix 4: Create TeamEventParticipation table
        if self.create_team_participation_table(dry_run):
            fixes_applied += 1
            
        # Fix 5: Update migration history
        if self.update_migration_history(dry_run):
            fixes_applied += 1
        
        if fixes_applied > 0:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Applied {fixes_applied} database fixes')
            )
            if not dry_run:
                self.stdout.write(
                    self.style.WARNING('🔄 Please restart your Django application')
                )
        else:
            self.stdout.write(
                self.style.SUCCESS('✅ Database schema is already up to date')
            )

    def column_exists(self, table_name, column_name):
        """Check if a column exists in a table"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND column_name = %s;
            """, [table_name, column_name])
            return cursor.fetchone() is not None

    def table_exists(self, table_name):
        """Check if a table exists"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = %s;
            """, [table_name])
            return cursor.fetchone() is not None

    def add_participation_type_column(self, dry_run=False):
        """Add participation_type column to core_event"""
        if self.column_exists('core_event', 'participation_type'):
            self.stdout.write("✅ participation_type column already exists")
            return False
            
        if dry_run:
            self.stdout.write("Would add participation_type column to core_event")
            return True
            
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    ALTER TABLE core_event 
                    ADD COLUMN participation_type VARCHAR(20) DEFAULT 'team';
                """)
            self.stdout.write("✅ Added participation_type column")
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to add participation_type: {e}")
            )
            return False

    def add_individual_points_multiplier(self, dry_run=False):
        """Add individual_points_multiplier column to core_event"""
        if self.column_exists('core_event', 'individual_points_multiplier'):
            self.stdout.write("✅ individual_points_multiplier column already exists")
            return False
            
        if dry_run:
            self.stdout.write("Would add individual_points_multiplier column to core_event")
            return True
            
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    ALTER TABLE core_event 
                    ADD COLUMN individual_points_multiplier DECIMAL(5,2) DEFAULT 1.0;
                """)
            self.stdout.write("✅ Added individual_points_multiplier column")
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to add individual_points_multiplier: {e}")
            )
            return False

    def add_eventscore_fields(self, dry_run=False):
        """Add missing fields to core_eventscore"""
        changes = 0
        
        # Add points_per_participant
        if not self.column_exists('core_eventscore', 'points_per_participant'):
            if dry_run:
                self.stdout.write("Would add points_per_participant column")
                changes += 1
            else:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            ALTER TABLE core_eventscore 
                            ADD COLUMN points_per_participant DECIMAL(5,2) DEFAULT 0;
                        """)
                    self.stdout.write("✅ Added points_per_participant column")
                    changes += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Failed to add points_per_participant: {e}")
                    )
        
        # Add auto_calculate_points
        if not self.column_exists('core_eventscore', 'auto_calculate_points'):
            if dry_run:
                self.stdout.write("Would add auto_calculate_points column")
                changes += 1
            else:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            ALTER TABLE core_eventscore 
                            ADD COLUMN auto_calculate_points BOOLEAN DEFAULT FALSE;
                        """)
                    self.stdout.write("✅ Added auto_calculate_points column")
                    changes += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Failed to add auto_calculate_points: {e}")
                    )
        
        if changes == 0:
            self.stdout.write("✅ EventScore fields already exist")
            
        return changes > 0

    def create_team_participation_table(self, dry_run=False):
        """Create core_teameventparticipation table"""
        if self.table_exists('core_teameventparticipation'):
            self.stdout.write("✅ TeamEventParticipation table already exists")
            return False
            
        if dry_run:
            self.stdout.write("Would create core_teameventparticipation table")
            return True
            
        try:
            with connection.cursor() as cursor:
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
            self.stdout.write("✅ Created TeamEventParticipation table")
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to create TeamEventParticipation table: {e}")
            )
            return False

    def update_migration_history(self, dry_run=False):
        """Mark migrations as applied in django_migrations table"""
        if dry_run:
            self.stdout.write("Would update migration history")
            return True
            
        try:
            with connection.cursor() as cursor:
                migrations = [
                    ('core', '0010_individual_event_models'),
                    ('core', '0011_fix_individual_vote_null_fields'),
                    ('core', '0012_team_event_participation'),
                ]
                
                for app, migration in migrations:
                    cursor.execute("""
                        INSERT INTO django_migrations (app, name, applied) 
                        VALUES (%s, %s, NOW()) 
                        ON CONFLICT (app, name) DO NOTHING;
                    """, [app, migration])
                    
            self.stdout.write("✅ Updated migration history")
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to update migration history: {e}")
            )
            return False
