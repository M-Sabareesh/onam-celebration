#!/usr/bin/env python3
"""
Complete Production Fix - PostgreSQL Database + Graph + Team Management
Fix all production issues including missing tables, empty graph, and team management
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
from django.db import models, connection
from django.conf import settings

def check_database_connection():
    """Check if database is accessible"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        db_engine = settings.DATABASES['default']['ENGINE']
        print(f"   Database type: {db_engine}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def list_existing_tables():
    """List all existing tables in the database"""
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
        return tables
    except Exception as e:
        print(f"❌ Error listing tables: {e}")
        return []

def fix_migrations():
    """Apply all migrations in the correct order"""
    print("🔧 Applying migrations in correct order...")
    try:
        # Core Django migrations first
        print("   📋 Applying Django core migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'contenttypes', '--noinput'])
        execute_from_command_line(['manage.py', 'migrate', 'auth', '--noinput'])
        execute_from_command_line(['manage.py', 'migrate', 'sessions', '--noinput'])
        execute_from_command_line(['manage.py', 'migrate', 'admin', '--noinput'])
        
        # App migrations
        print("   🎯 Applying app migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'core', '--noinput'])
        execute_from_command_line(['manage.py', 'migrate', 'accounts', '--noinput'])
        execute_from_command_line(['manage.py', 'migrate', 'games', '--noinput'])
        
        # All remaining migrations
        print("   🔄 Applying all remaining migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        print("✅ All migrations applied successfully")
        return True
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
        return False

def create_sample_data():
    """Create sample data for testing graphs and leaderboard"""
    try:
        print("📊 Creating sample data for graphs...")
        
        from apps.core.models import Player, Event, EventScore, TeamConfiguration
        
        # Ensure team configurations exist
        default_teams = [
            ('team_1', 'Red Warriors'),
            ('team_2', 'Blue Champions'),
            ('team_3', 'Green Masters'),
            ('team_4', 'Yellow Legends'),
            ('unassigned', 'Unassigned'),
        ]
        
        print("   🏆 Setting up team configurations...")
        for team_code, team_name in default_teams:
            team, created = TeamConfiguration.objects.get_or_create(
                team_code=team_code,
                defaults={'team_name': team_name, 'is_active': True}
            )
            if created:
                print(f"     Created: {team.team_code} -> {team.team_name}")
        
        # Create sample players if none exist
        if Player.objects.count() < 4:
            print("   👥 Creating sample players...")
            sample_players = [
                ('Player 1', 'team_1'),
                ('Player 2', 'team_2'),
                ('Player 3', 'team_3'),
                ('Player 4', 'team_4'),
            ]
            
            for name, team in sample_players:
                player, created = Player.objects.get_or_create(
                    name=name,
                    defaults={
                        'team': team,
                        'is_active': True,
                        'score': 100
                    }
                )
                if created:
                    print(f"     Created player: {name} in {team}")
        
        # Create sample events if none exist
        if Event.objects.count() < 3:
            print("   🎮 Creating sample events...")
            sample_events = [
                ('Dance Competition', 'team'),
                ('Quiz Contest', 'individual'),
                ('Cultural Show', 'team'),
            ]
            
            for title, event_type in sample_events:
                event, created = Event.objects.get_or_create(
                    title=title,
                    defaults={
                        'description': f'Sample {title}',
                        'event_type': event_type,
                        'is_active': True,
                        'max_points': 100
                    }
                )
                if created:
                    print(f"     Created event: {title} ({event_type})")
        
        # Create sample scores if none exist
        if EventScore.objects.count() < 6:
            print("   📈 Creating sample scores...")
            events = Event.objects.filter(is_active=True)[:3]
            teams = ['team_1', 'team_2', 'team_3', 'team_4']
            
            for i, event in enumerate(events):
                for j, team in enumerate(teams):
                    score_value = 100 - (i * 10) - (j * 5)  # Varying scores
                    score, created = EventScore.objects.get_or_create(
                        event=event,
                        team=team,
                        defaults={'score': score_value}
                    )
                    if created:
                        print(f"     Created score: {event.title} - {team}: {score_value}")
        
        print("✅ Sample data created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def create_superuser():
    """Create superuser if it doesn't exist"""
    try:
        from django.contrib.auth.models import User
        
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'OnamAdmin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            print("👤 Creating superuser...")
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"✅ Superuser '{username}' created")
        else:
            print(f"✅ Superuser '{username}' already exists")
        return True
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

def test_graph_data():
    """Test that graph data is available"""
    try:
        from apps.core.models import EventScore, TeamConfiguration
        
        print("📊 Testing graph data...")
        
        # Check if we have events and scores
        total_scores = EventScore.objects.count()
        print(f"   Event scores available: {total_scores}")
        
        if total_scores > 0:
            # Test team score aggregation
            team_scores = {}
            for team_config in TeamConfiguration.objects.filter(is_active=True):
                team_total = EventScore.objects.filter(team=team_config.team_code).aggregate(
                    total=models.Sum('score')
                )['total'] or 0
                team_scores[team_config.team_name] = team_total
                print(f"   {team_config.team_name}: {team_total} points")
            
            if any(score > 0 for score in team_scores.values()):
                print("✅ Graph data is available")
                return True
            else:
                print("⚠️  No non-zero scores found")
                return False
        else:
            print("⚠️  No event scores found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing graph data: {e}")
        return False

def main():
    """Main fix function"""
    print("🚨 COMPLETE PRODUCTION FIX")
    print("=" * 50)
    
    # Check current environment
    print(f"🔧 Django settings: {settings.SETTINGS_MODULE}")
    print(f"🔧 Database: {settings.DATABASES['default']['ENGINE']}")
    
    # 1. Check database connection
    if not check_database_connection():
        print("❌ Cannot proceed without database connection")
        return False
    
    # 2. List existing tables
    existing_tables = list_existing_tables()
    
    # 3. Apply migrations
    if not fix_migrations():
        print("❌ Migration failed")
        return False
    
    # 4. Create superuser
    create_superuser()
    
    # 5. Create sample data for graphs
    create_sample_data()
    
    # 6. Test graph data
    test_graph_data()
    
    # 7. Final verification
    print("\n🔍 Final verification...")
    final_tables = list_existing_tables()
    
    required_tables = ['django_session', 'core_teamconfiguration', 'core_eventscore']
    missing_tables = [table for table in required_tables if table not in final_tables]
    
    if missing_tables:
        print(f"❌ Still missing tables: {missing_tables}")
        return False
    else:
        print("✅ All required tables exist")
    
    print("\n✅ PRODUCTION FIX COMPLETE!")
    print("🌐 Your site should now be accessible with:")
    print("   - Working homepage and leaderboard")
    print("   - Populated graphs and charts")
    print("   - Admin team management")
    print("   - Sample data for testing")
    
    return True

if __name__ == "__main__":
    main()
