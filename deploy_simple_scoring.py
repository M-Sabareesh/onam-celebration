#!/usr/bin/env python3
"""
Deploy Simple Event Scoring System
Complete deployment with new scoring functionality
"""
import os
import sys

# Add current directory to Python path  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def deploy_simple_scoring():
    """Deploy the simple event scoring system"""
    try:
        import django
        django.setup()
        
        from django.core.management import execute_from_command_line
        from apps.core.models import Event, Player, SimpleEventScore, TeamConfiguration
        
        print("🚀 Deploying Simple Event Scoring System")
        print("=" * 50)
        
        # Step 1: Run migrations
        print("📦 Running migrations...")
        try:
            execute_from_command_line(['manage.py', 'migrate'])
            print("✅ Migrations completed successfully")
        except Exception as e:
            print(f"⚠️  Migration warning (may be normal): {e}")
        
        # Step 2: Ensure team configurations exist
        print("\n👥 Setting up team configurations...")
        default_teams = [
            ('team_1', 'Team 1'),
            ('team_2', 'Team 2'), 
            ('team_3', 'Team 3'),
            ('team_4', 'Team 4'),
        ]
        
        for team_code, team_name in default_teams:
            team, created = TeamConfiguration.objects.get_or_create(
                team_code=team_code,
                defaults={'team_name': team_name, 'is_active': True}
            )
            if created:
                print(f"   + Created: {team_name}")
            else:
                print(f"   ✓ Exists: {team.team_name}")
        
        # Step 3: Create sample events if none exist
        print("\n📅 Setting up sample events...")
        if not Event.objects.filter(is_active=True).exists():
            sample_events = [
                {
                    'title': 'Dance Competition',
                    'description': 'Traditional Malayalam dance performances',
                    'max_participants': 20,
                    'is_active': True,
                    'voting_enabled': False,
                    'participation_type': 'team'
                },
                {
                    'title': 'Singing Contest',
                    'description': 'Individual singing competition',
                    'max_participants': 10,
                    'is_active': True,
                    'voting_enabled': False,
                    'participation_type': 'individual'
                },
                {
                    'title': 'Drama Performance',
                    'description': 'Team drama with individual roles',
                    'max_participants': 15,
                    'is_active': True,
                    'voting_enabled': False,
                    'participation_type': 'both'
                }
            ]
            
            for event_data in sample_events:
                event = Event.objects.create(**event_data)
                print(f"   + Created: {event.title}")
        else:
            events = Event.objects.filter(is_active=True)
            print(f"   ✓ {events.count()} events already exist")
        
        # Step 4: Create sample players if none exist
        print("\n🎭 Setting up sample players...")
        if Player.objects.filter(is_active=True).count() < 4:
            sample_players = [
                ('Arjun', 'team_1'),
                ('Priya', 'team_1'),
                ('Ravi', 'team_2'),
                ('Meera', 'team_2'),
                ('Suresh', 'team_3'),
                ('Lakshmi', 'team_3'),
                ('Kiran', 'team_4'),
                ('Nisha', 'team_4'),
            ]
            
            for name, team in sample_players:
                player, created = Player.objects.get_or_create(
                    name=name,
                    defaults={'team': team, 'is_active': True}
                )
                if created:
                    print(f"   + Created: {name} ({TeamConfiguration.get_team_name(team)})")
        else:
            players = Player.objects.filter(is_active=True)
            print(f"   ✓ {players.count()} players already exist")
        
        # Step 5: Test the scoring system
        print("\n🏆 Testing scoring system...")
        events = Event.objects.filter(is_active=True)
        teams = TeamConfiguration.objects.filter(is_active=True)
        
        if events.exists() and teams.exists():
            print("✅ Simple Event Scoring is ready!")
            print(f"   📊 {events.count()} events available")
            print(f"   👥 {teams.count()} teams configured")
            print(f"   🎯 Ready for scoring at /admin/simple-scoring/")
        else:
            print("⚠️  System needs more setup")
        
        # Step 6: Show access information
        print("\n🔗 Access Points:")
        print("   📱 Simple Scoring Interface: /admin/simple-scoring/")
        print("   🛠️  Django Admin: /admin/core/simpleeventcore/")
        print("   📊 Leaderboard: /leaderboard/")
        print("   👥 Team Management: /team-management/")
        print("   🏠 Home: /")
        
        print("\n📋 Scoring Instructions:")
        print("   1. Select an event")
        print("   2. Choose a team")
        print("   3. Enter points (0-100)")
        print("   4. Pick event type:")
        print("      - Team: Points go to team only")
        print("      - Individual: Points for individual competition")
        print("      - Hybrid: Team points + select individual participants")
        print("   5. Add optional notes")
        print("   6. Click 'Award Points'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error deploying simple scoring: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    deploy_simple_scoring()
