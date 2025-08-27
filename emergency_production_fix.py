#!/usr/bin/env python3
"""
EMERGENCY PRODUCTION FIX - Missing TeamConfiguration Table
Fix the missing core_teamconfiguration table and other database issues
"""

import os
import sys
import django
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

try:
    django.setup()
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    print("Trying with development settings...")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'onam_project.settings.development'
    django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def check_database_tables():
    """Check which tables exist in the database"""
    try:
        with connection.cursor() as cursor:
            db_engine = settings.DATABASES['default']['ENGINE']
            
            if 'postgresql' in db_engine:
                cursor.execute("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public' 
                    ORDER BY tablename;
                """)
            else:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' 
                    ORDER BY name;
                """)
            
            tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📋 Found {len(tables)} existing tables:")
        for table in tables:
            print(f"   - {table}")
        
        # Check for critical missing tables
        missing_tables = []
        required_tables = [
            'django_session',
            'auth_user',
            'core_player',
            'core_teamconfiguration',
            'core_event',
            'core_eventscore'
        ]
        
        for table in required_tables:
            if table not in tables:
                missing_tables.append(table)
        
        if missing_tables:
            print(f"\n❌ Missing critical tables: {missing_tables}")
            return False, missing_tables
        else:
            print("\n✅ All critical tables exist")
            return True, []
            
    except Exception as e:
        print(f"❌ Error checking database tables: {e}")
        return False, []

def apply_migrations_safely():
    """Apply migrations in the correct order with error handling"""
    print("🔧 Applying migrations safely...")
    
    migration_steps = [
        ('contenttypes', 'Content Types'),
        ('auth', 'Authentication'),
        ('sessions', 'Sessions'),
        ('admin', 'Admin'),
        ('core', 'Core App'),
        ('accounts', 'Accounts'),
        ('games', 'Games'),
    ]
    
    for app, description in migration_steps:
        try:
            print(f"   📋 Applying {description} migrations...")
            execute_from_command_line(['manage.py', 'migrate', app, '--noinput'])
            print(f"   ✅ {description} migrations applied")
        except Exception as e:
            print(f"   ⚠️  {description} migration failed: {e}")
            if app in ['core']:  # Critical apps
                print(f"   🔄 Retrying {description} migrations...")
                try:
                    execute_from_command_line(['manage.py', 'migrate', app, '--fake-initial', '--noinput'])
                    print(f"   ✅ {description} migrations applied with fake-initial")
                except Exception as e2:
                    print(f"   ❌ {description} migration still failed: {e2}")
    
    # Apply all remaining migrations
    try:
        print("   🔄 Applying all remaining migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("   ✅ All migrations applied")
    except Exception as e:
        print(f"   ⚠️  Some migrations failed: {e}")

def create_missing_tables_manually():
    """Manually create missing tables if migrations fail"""
    print("🛠️  Creating missing tables manually...")
    
    try:
        with connection.cursor() as cursor:
            # Create core_teamconfiguration table
            print("   📋 Creating core_teamconfiguration table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_teamconfiguration (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_code VARCHAR(20) UNIQUE NOT NULL,
                    team_name VARCHAR(100) NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create core_event table if missing
            print("   📋 Creating core_event table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_event (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    event_type VARCHAR(20) DEFAULT 'team',
                    is_active BOOLEAN DEFAULT 1,
                    max_points INTEGER DEFAULT 100,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create core_eventscore table if missing
            print("   📋 Creating core_eventscore table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_eventscore (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER NOT NULL,
                    team VARCHAR(20) NOT NULL,
                    score DECIMAL(5,2) DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (event_id) REFERENCES core_event (id)
                );
            """)
            
            print("   ✅ Critical tables created manually")
            
    except Exception as e:
        print(f"   ❌ Error creating tables manually: {e}")

def setup_team_configurations():
    """Setup team configurations with error handling"""
    print("🏆 Setting up team configurations...")
    
    try:
        # Import after ensuring tables exist
        from apps.core.models import TeamConfiguration
        
        default_teams = [
            ('team_1', 'Red Warriors'),
            ('team_2', 'Blue Champions'),
            ('team_3', 'Green Masters'),
            ('team_4', 'Yellow Legends'),
            ('unassigned', 'Unassigned'),
        ]
        
        created_count = 0
        for team_code, team_name in default_teams:
            try:
                team, created = TeamConfiguration.objects.get_or_create(
                    team_code=team_code,
                    defaults={'team_name': team_name, 'is_active': True}
                )
                if created:
                    created_count += 1
                print(f"   ✅ {team.team_code}: {team.team_name}")
            except Exception as e:
                print(f"   ❌ Error creating team {team_code}: {e}")
        
        print(f"   🎯 Team configurations ready ({created_count} new teams created)")
        return True
        
    except Exception as e:
        print(f"   ❌ Error setting up teams: {e}")
        return False

def create_sample_data():
    """Create minimal sample data for testing"""
    print("📊 Creating sample data...")
    
    try:
        from apps.core.models import Player, Event, EventScore
        
        # Create sample players
        if Player.objects.count() < 4:
            sample_players = [
                ('Test Player 1', 'team_1'),
                ('Test Player 2', 'team_2'),
                ('Test Player 3', 'team_3'),
                ('Test Player 4', 'team_4'),
            ]
            
            for name, team in sample_players:
                player, created = Player.objects.get_or_create(
                    name=name,
                    defaults={'team': team, 'is_active': True, 'score': 50}
                )
                if created:
                    print(f"   👤 Created player: {name}")
        
        # Create sample events
        if Event.objects.count() < 2:
            sample_events = [
                ('Dance Competition', 'team'),
                ('Singing Contest', 'individual'),
            ]
            
            for title, event_type in sample_events:
                event, created = Event.objects.get_or_create(
                    title=title,
                    defaults={'event_type': event_type, 'is_active': True}
                )
                if created:
                    print(f"   🎭 Created event: {title}")
        
        print("   ✅ Sample data created")
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating sample data: {e}")
        return False

def create_superuser():
    """Create superuser with error handling"""
    try:
        from django.contrib.auth.models import User
        
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'OnamAdmin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"✅ Superuser '{username}' created")
        else:
            print(f"✅ Superuser '{username}' already exists")
            
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

def main():
    """Main emergency fix function"""
    print("🚨 EMERGENCY PRODUCTION FIX")
    print("=" * 50)
    
    # Check current environment
    print(f"🔧 Django settings: {settings.SETTINGS_MODULE}")
    print(f"🔧 Database: {settings.DATABASES['default']['ENGINE']}")
    
    # 1. Check database tables
    all_tables_exist, missing_tables = check_database_tables()
    
    # 2. Apply migrations if tables are missing
    if not all_tables_exist:
        apply_migrations_safely()
        
        # 3. Check again after migrations
        all_tables_exist, missing_tables = check_database_tables()
        
        # 4. Create tables manually if migrations failed
        if not all_tables_exist:
            create_missing_tables_manually()
    
    # 5. Setup team configurations
    setup_team_configurations()
    
    # 6. Create sample data
    create_sample_data()
    
    # 7. Create superuser
    create_superuser()
    
    # 8. Final verification
    print("\n🔍 Final verification...")
    final_check, final_missing = check_database_tables()
    
    if final_check:
        print("✅ EMERGENCY FIX COMPLETE!")
        print("🌐 Your site should now be accessible")
        print("🏆 Team management available at /admin/")
    else:
        print(f"❌ Some issues remain: {final_missing}")
        print("🔄 You may need to check your database configuration")
    
    return final_check

if __name__ == "__main__":
    main()
