#!/usr/bin/env python
"""
Production Migration Fix for Render Deployment
This script safely applies the missing migrations in production.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection, transaction

def setup_django():
    """Setup Django environment for production"""
    # Use production settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
    django.setup()

def check_database_status():
    """Check what migrations are missing"""
    print("🔍 Checking database status...")
    
    try:
        with connection.cursor() as cursor:
            # Check if participation_type column exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'core_event' 
                AND column_name = 'participation_type';
            """)
            has_participation_type = cursor.fetchone() is not None
            
            # Check if TeamEventParticipation table exists
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'core_teameventparticipation';
            """)
            has_team_participation = cursor.fetchone() is not None
            
            print(f"participation_type column: {'✅ EXISTS' if has_participation_type else '❌ MISSING'}")
            print(f"TeamEventParticipation table: {'✅ EXISTS' if has_team_participation else '❌ MISSING'}")
            
            return has_participation_type, has_team_participation
            
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False, False

def check_migration_status():
    """Check which migrations have been applied"""
    print("\n🔍 Checking migration status...")
    
    try:
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        
        # Get applied migrations
        applied = executor.loader.applied_migrations
        
        # Check specific migrations we need
        migrations_to_check = [
            ('core', '0010_individual_event_models'),
            ('core', '0011_fix_individual_vote_null_fields'),
            ('core', '0012_team_event_participation'),
        ]
        
        for app, migration in migrations_to_check:
            is_applied = (app, migration) in applied
            status = "✅ APPLIED" if is_applied else "❌ MISSING"
            print(f"  {migration}: {status}")
            
        return applied
        
    except Exception as e:
        print(f"❌ Migration check failed: {e}")
        return set()

def run_specific_migrations():
    """Run the specific migrations needed"""
    print("\n🔄 Applying missing migrations...")
    
    # List of migrations to apply in order
    migrations_to_apply = [
        ('core', '0010'),  # Adds participation_type and individual event models
        ('core', '0011'),  # Fixes individual vote null fields
        ('core', '0012'),  # Adds TeamEventParticipation model
    ]
    
    success_count = 0
    
    for app, migration_number in migrations_to_apply:
        try:
            print(f"🔄 Applying {app} {migration_number}...")
            execute_from_command_line(['manage.py', 'migrate', app, migration_number])
            print(f"✅ Successfully applied {app} {migration_number}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to apply {app} {migration_number}: {e}")
            # Continue with other migrations even if one fails
    
    # Apply any remaining migrations
    try:
        print("🔄 Applying any remaining migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ All migrations completed")
        success_count += 1
    except Exception as e:
        print(f"⚠️ Final migrate command had issues: {e}")
    
    return success_count > 0

def create_backup():
    """Create a database backup before migrations (if possible)"""
    print("\n💾 Creating database backup...")
    
    try:
        # Create a data dump of critical models
        execute_from_command_line(['manage.py', 'dumpdata', 'core.Player', 'core.Event', 'core.EventScore', '--output=backup_before_migration.json'])
        print("✅ Backup created: backup_before_migration.json")
        return True
    except Exception as e:
        print(f"⚠️ Backup failed (not critical): {e}")
        return False

def verify_fix():
    """Verify that the fix worked"""
    print("\n🔍 Verifying fix...")
    
    try:
        # Try to import and use the models
        from apps.core.models import Event, TeamEventParticipation
        
        # Test accessing the participation_type field
        event_count = Event.objects.count()
        print(f"✅ Can access Event model: {event_count} events found")
        
        # Test accessing TeamEventParticipation
        participation_count = TeamEventParticipation.objects.count()
        print(f"✅ Can access TeamEventParticipation model: {participation_count} records found")
        
        # Test creating a simple query with participation_type
        team_events = Event.objects.filter(participation_type='team').count()
        print(f"✅ Can query participation_type field: {team_events} team events found")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main execution function"""
    print("🔧 Production Migration Fix for Onam Celebration")
    print("=" * 50)
    
    # Setup Django
    setup_django()
    
    # Create backup
    create_backup()
    
    # Check current status
    has_participation_type, has_team_participation = check_database_status()
    applied_migrations = check_migration_status()
    
    # Only run migrations if needed
    if not has_participation_type or not has_team_participation:
        print("\n🚨 Missing database columns/tables detected. Running migrations...")
        
        success = run_specific_migrations()
        
        if success:
            print("\n🔍 Re-checking database status...")
            has_participation_type, has_team_participation = check_database_status()
            
            if has_participation_type and has_team_participation:
                print("\n✅ Migration successful!")
                
                # Verify the fix works
                if verify_fix():
                    print("\n🎉 All systems operational!")
                    print("\nFeatures now available:")
                    print("• Team event participation tracking")
                    print("• Checkbox selection of participants")
                    print("• Auto-calculation of points based on participant count")
                    print("• Enhanced admin interface")
                else:
                    print("\n⚠️ Migrations applied but verification failed")
            else:
                print("\n❌ Migrations completed but database issues remain")
        else:
            print("\n❌ Migration failed")
    else:
        print("\n✅ Database is already up to date!")
        if verify_fix():
            print("🎉 All systems operational!")
        else:
            print("⚠️ Database columns exist but there may be other issues")

if __name__ == '__main__':
    main()
