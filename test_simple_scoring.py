#!/usr/bin/env python3
"""
Test Simple Event Scoring System
"""
import os
import sys

# Add current directory to Python path  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def test_simple_scoring():
    """Test the simple event scoring system"""
    try:
        import django
        django.setup()
        
        from apps.core.models import Event, Player, SimpleEventScore, TeamConfiguration
        
        print("🎯 Testing Simple Event Scoring System")
        print("=" * 50)
        
        # Check if we have events
        events = Event.objects.filter(is_active=True)
        print(f"📅 Active Events: {events.count()}")
        for event in events[:3]:
            print(f"   - {event.title}")
        
        # Check teams
        teams = TeamConfiguration.objects.filter(is_active=True)
        print(f"\n👥 Active Teams: {teams.count()}")
        for team in teams:
            player_count = Player.objects.filter(team=team.team_code, is_active=True).count()
            print(f"   - {team.team_name} ({team.team_code}): {player_count} players")
        
        # Check existing scores
        scores = SimpleEventScore.objects.all()
        print(f"\n🏆 Existing Simple Scores: {scores.count()}")
        for score in scores[:5]:
            print(f"   - {score.event.title}: {score.get_team_display()} = {score.points} pts")
        
        # Test creating a sample score if we have data
        if events.exists() and teams.exists():
            print(f"\n✅ System is ready for scoring!")
            print(f"   📱 Access the scoring interface at: /admin/simple-scoring/")
            print(f"   🔧 Or use Django Admin: /admin/core/simpleeventcore/")
            
            # Show some sample scoring scenarios
            print(f"\n📝 Sample Scoring Scenarios:")
            print(f"   1. Team Event: Select event + team + points")
            print(f"   2. Individual Event: Select event + team + points (individual scores)")
            print(f"   3. Hybrid Event: Select event + team + points + individual participants")
        else:
            print(f"\n⚠️  Setup needed:")
            if not events.exists():
                print(f"   - Create some events first")
            if not teams.exists():
                print(f"   - Set up team configurations")
        
        print(f"\n🔗 Quick Links:")
        print(f"   - Home: /")
        print(f"   - Leaderboard: /leaderboard/")
        print(f"   - Team Management: /team-management/")
        print(f"   - Simple Scoring: /admin/simple-scoring/")
        print(f"   - Django Admin: /admin/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing simple scoring: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_simple_scoring()
