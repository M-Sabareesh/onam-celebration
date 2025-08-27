#!/usr/bin/env python3
"""
Test Team Administration Feature
Test the team name management functionality in Django admin
"""

import os
import sys
import django

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

from apps.core.models import TeamConfiguration, Player

def test_team_admin():
    """Test team administration functionality"""
    print("🎯 Testing Team Administration Feature")
    print("=" * 50)
    
    # 1. Check if TeamConfiguration model is accessible
    print("1. Checking TeamConfiguration model...")
    try:
        team_count = TeamConfiguration.objects.count()
        print(f"   ✅ TeamConfiguration model accessible - {team_count} teams found")
    except Exception as e:
        print(f"   ❌ Error accessing TeamConfiguration: {e}")
        return False
    
    # 2. Create/verify default teams
    print("\n2. Setting up default teams...")
    default_teams = [
        ('team_1', 'Team 1'),
        ('team_2', 'Team 2'),
        ('team_3', 'Team 3'),
        ('team_4', 'Team 4'),
        ('unassigned', 'Unassigned'),
    ]
    
    for team_code, team_name in default_teams:
        team, created = TeamConfiguration.objects.get_or_create(
            team_code=team_code,
            defaults={'team_name': team_name, 'is_active': True}
        )
        status = "Created" if created else "Exists"
        print(f"   {status}: {team.team_code} -> {team.team_name}")
    
    # 3. Test team name retrieval
    print("\n3. Testing team name retrieval...")
    teams = TeamConfiguration.objects.filter(is_active=True).order_by('team_code')
    for team in teams:
        print(f"   {team.team_code}: {team.team_name} (Active: {team.is_active})")
    
    # 4. Test dynamic team choices
    print("\n4. Testing dynamic team choices...")
    choices = TeamConfiguration.get_team_choices()
    print("   Team choices for forms:")
    for code, name in choices:
        print(f"     {code} -> {name}")
    
    # 5. Test team name lookup
    print("\n5. Testing team name lookup...")
    test_codes = ['team_1', 'team_2', 'team_3', 'invalid_team']
    for code in test_codes:
        name = TeamConfiguration.get_team_name(code)
        print(f"   {code} -> {name}")
    
    # 6. Check players using team names
    print("\n6. Checking player assignments...")
    players = Player.objects.filter(is_active=True)
    team_counts = {}
    for player in players:
        team_name = TeamConfiguration.get_team_name(player.team)
        team_counts[team_name] = team_counts.get(team_name, 0) + 1
    
    print("   Player distribution by team:")
    for team_name, count in team_counts.items():
        print(f"     {team_name}: {count} players")
    
    print("\n7. Testing admin interface availability...")
    print("   ℹ️  To test admin interface:")
    print("      1. Start Django server: python manage.py runserver")
    print("      2. Go to: http://localhost:8000/admin/")
    print("      3. Navigate to: Core > Team configurations")
    print("      4. Edit team names and save")
    print("      5. Check leaderboard to see updated names")
    
    print("\n✅ Team Administration Test Complete!")
    print("   You can now change team names through Django admin panel.")
    return True

if __name__ == "__main__":
    test_team_admin()
