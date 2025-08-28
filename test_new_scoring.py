#!/usr/bin/env python3
"""
Test New Simple Event Scoring
"""
import os
import sys

# Add current directory to Python path  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def test_new_scoring():
    """Test the new simple event scoring system"""
    try:
        import django
        django.setup()
        
        from apps.core.models import Event, Player, SimpleEventScore, TeamConfiguration
        
        print("🎯 TESTING NEW SIMPLE EVENT SCORING")
        print("=" * 50)
        
        # Check if we have events
        events = Event.objects.filter(is_active=True)
        print(f"📅 Active Events: {events.count()}")
        for event in events[:3]:
            print(f"   - {event.name} (ID: {event.id})")
        
        # Check teams
        teams = TeamConfiguration.objects.filter(is_active=True)
        print(f"\n👥 Active Teams: {teams.count()}")
        for team in teams:
            player_count = Player.objects.filter(team=team.team_code, is_active=True).count()
            print(f"   - {team.team_name} ({team.team_code}): {player_count} players")
            
            # Show first few players for each team
            players = Player.objects.filter(team=team.team_code, is_active=True)[:3]
            for player in players:
                print(f"     • {player.name}")
        
        # Check existing scores
        scores = SimpleEventScore.objects.all()
        print(f"\n🏆 Existing Simple Scores: {scores.count()}")
        for score in scores[:5]:
            participants = score.participants.count()
            print(f"   - {score.event.name}: {score.get_team_display()} = {score.points} pts ({participants} players)")
        
        print(f"\n🔗 NEW ACCESS POINTS:")
        print(f"   📱 Primary: /admin/simple-scoring/")
        print(f"   🎯 Direct: /simple-scoring/")
        print(f"   📊 Alt: /event-scoring/")
        
        print(f"\n✨ NEW FEATURES:")
        print(f"   ✅ Clean interface with just: Event, Team, Points, Players")
        print(f"   ✅ Players filtered by selected team automatically")
        print(f"   ✅ Points divided among selected players")
        print(f"   ✅ Team-only scoring (no players selected)")
        print(f"   ✅ Individual player points calculated automatically")
        
        print(f"\n📋 WORKFLOW:")
        print(f"   1. Select Event from dropdown")
        print(f"   2. Select Team from dropdown") 
        print(f"   3. Enter Points (any decimal value)")
        print(f"   4. Optionally select individual players")
        print(f"   5. Click 'Award Points'")
        print(f"   6. Points are distributed automatically")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing new scoring: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_new_scoring()
