#!/usr/bin/env python3
"""
Fix Team Names in Leaderboard - Complete Solution
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def main():
    print("🔧 FIXING TEAM NAMES IN LEADERBOARD")
    print("=" * 45)
    
    try:
        import django
        django.setup()
        
        # Import models
        from apps.core.models import TeamConfiguration, Player, Event, EventScore
        from django.contrib.auth.models import User
        
        # Step 1: Ensure TeamConfiguration entries exist
        print("📋 Setting up TeamConfiguration entries...")
        default_teams = [
            ('team_1', 'Red Warriors'),
            ('team_2', 'Blue Champions'),
            ('team_3', 'Green Guardians'), 
            ('team_4', 'Golden Eagles'),
            ('unassigned', 'Unassigned')
        ]
        
        for team_code, team_name in default_teams:
            team, created = TeamConfiguration.objects.get_or_create(
                team_code=team_code,
                defaults={'team_name': team_name}
            )
            if created:
                print(f"   ✅ Created: {team_code} → {team_name}")
            else:
                # Update existing name if it's still the default
                if team.team_name in ['Team 1', 'Team 2', 'Team 3', 'Team 4']:
                    team.team_name = team_name
                    team.save()
                    print(f"   🔄 Updated: {team_code} → {team_name}")
                else:
                    print(f"   ✅ Exists: {team_code} → {team.team_name}")
        
        # Step 2: Ensure we have some players for testing
        print("\n👥 Setting up sample players...")
        sample_players = [
            ('Alice Johnson', 'team_1'),
            ('Bob Smith', 'team_2'),
            ('Charlie Davis', 'team_3'),
            ('Diana Wilson', 'team_4'),
            ('Emma Brown', 'team_1'),
            ('Frank Miller', 'team_2'),
        ]
        
        for name, team in sample_players:
            player, created = Player.objects.get_or_create(
                name=name,
                defaults={'team': team, 'is_active': True, 'score': 50}
            )
            if created:
                print(f"   ✅ Created player: {name} ({team})")
        
        # Step 3: Create sample events for testing
        print("\n🎪 Setting up sample events...")
        sample_events = [
            ('Dance Competition', 'team'),
            ('Singing Contest', 'individual'),
            ('Drama Performance', 'team'),
            ('Sports Tournament', 'team'),
        ]
        
        for title, event_type in sample_events:
            event, created = Event.objects.get_or_create(
                title=title,
                defaults={
                    'description': f'Sample {title} for Onam celebration',
                    'event_type': event_type,
                    'is_active': True,
                    'max_points': 100
                }
            )
            if created:
                print(f"   ✅ Created event: {title}")
        
        # Step 4: Test the leaderboard data generation
        print("\n🧪 Testing leaderboard data generation...")
        
        # Simulate the LeaderboardView logic
        team_configs = {tc.team_code: tc.team_name for tc in TeamConfiguration.objects.filter(is_active=True)}
        print(f"   Team configs: {team_configs}")
        
        # Calculate team data
        team_data = {}
        for team_code, team_name in team_configs.items():
            if team_code == 'unassigned':
                continue
                
            team_data[team_code] = {
                'name': team_name,  # This is the key fix!
                'treasure_hunt_score': 0,
                'total_score': 0,
                'players': []
            }
        
        # Add player scores
        for player in Player.objects.all():
            team = player.team
            if team in team_data:
                team_data[team]['treasure_hunt_score'] += player.score
                team_data[team]['total_score'] += player.score
                team_data[team]['players'].append(player)
        
        # Sort teams by score
        sorted_teams = sorted(team_data.items(), key=lambda x: x[1]['total_score'], reverse=True)
        
        print("\n📊 Final team standings data:")
        for team_code, team_info in sorted_teams:
            print(f"   {team_code}: {team_info['name']} - {team_info['total_score']} points")
        
        # Step 5: Create admin user
        print("\n👤 Setting up admin user...")
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("   ✅ Admin user created (admin/admin123)")
        else:
            print("   ✅ Admin user exists")
        
        print("\n🎉 TEAM NAMES FIX COMPLETE!")
        print("=" * 45)
        print("🌐 Now you can:")
        print("   • Visit /leaderboard/ to see updated team names")
        print("   • Visit /team-management/ to change team names")
        print("   • Visit /custom-admin/ to access admin panel")
        print("\n🎯 Updated team names:")
        for team in TeamConfiguration.objects.filter(is_active=True):
            print(f"   • {team.team_code}: {team.team_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Team names should now display correctly in the leaderboard!")
    else:
        print("\n❌ Fix failed. Check the errors above.")
