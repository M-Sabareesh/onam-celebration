#!/usr/bin/env python3
"""
Test Team Names in Leaderboard
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def main():
    print("🔍 TESTING TEAM NAMES IN LEADERBOARD")
    print("=" * 45)
    
    try:
        import django
        django.setup()
        
        from apps.core.models import TeamConfiguration, Player
        
        print("📋 Current TeamConfiguration entries:")
        for team in TeamConfiguration.objects.all():
            print(f"   {team.team_code}: {team.team_name}")
        
        print("\n👥 Current Player teams:")
        teams_used = set()
        for player in Player.objects.all()[:10]:
            teams_used.add(player.team)
            print(f"   {player.name}: {player.team}")
        
        print(f"\n🔍 Teams in use: {list(teams_used)}")
        
        # Test the team_configs dict that's passed to template
        print("\n📊 Testing leaderboard team_configs:")
        team_configs = {tc.team_code: tc.team_name for tc in TeamConfiguration.objects.filter(is_active=True)}
        for code, name in team_configs.items():
            print(f"   {code} → {name}")
        
        # Test the get_team_name method
        print("\n🧪 Testing get_team_name method:")
        for code in ['team_1', 'team_2', 'team_3', 'team_4']:
            name = TeamConfiguration.get_team_name(code)
            print(f"   {code} → {name}")
        
        # Simulate the leaderboard view logic
        print("\n🎯 Simulating leaderboard team_data creation:")
        team_data = {}
        for team_code, team_name in team_configs.items():
            if team_code == 'unassigned':
                continue
            team_data[team_code] = {
                'name': team_name,
                'total_score': 100,  # Sample score
                'players': []
            }
        
        # Sort teams by score (simulated)
        sorted_teams = sorted(team_data.items(), key=lambda x: x[1]['total_score'], reverse=True)
        
        print("\n📈 Template team_standings data:")
        for team_code, team_info in sorted_teams:
            print(f"   {team_code}: {team_info['name']} ({team_info['total_score']} pts)")
        
        print("\n✅ TEAM NAMES TEST COMPLETE!")
        
        # Create some test updates
        print("\n🔧 Updating sample team names...")
        test_names = {
            'team_1': 'Red Warriors',
            'team_2': 'Blue Champions',
            'team_3': 'Green Guardians',
            'team_4': 'Golden Eagles'
        }
        
        for team_code, new_name in test_names.items():
            team, created = TeamConfiguration.objects.get_or_create(
                team_code=team_code,
                defaults={'team_name': new_name}
            )
            if not created:
                team.team_name = new_name
                team.save()
            print(f"   ✅ {team_code} → {new_name}")
        
        print("\n🎉 Team names updated! Check your leaderboard now.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
