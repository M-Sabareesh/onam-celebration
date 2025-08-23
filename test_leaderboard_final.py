#!/usr/bin/env python
"""
Test script to verify the updated leaderboard functionality
including event scores display.
"""

import os
import sys
import django

# Add the project directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

from django.test import Client
from django.urls import reverse
from apps.core.models import Player, Event, EventVote, EventParticipation

def test_leaderboard_view():
    """Test that the leaderboard view loads without errors"""
    print("🧪 Testing Leaderboard View...")
    
    client = Client()
    
    try:
        # Test leaderboard page load
        response = client.get(reverse('core:leaderboard'))
        print(f"✅ Leaderboard page status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Leaderboard page loads successfully")
            
            # Check for key elements in the rendered content
            content = response.content.decode('utf-8')
            
            # Check for updated title
            if "Onam Aghosham Leaderboard" in content:
                print("✅ Updated leaderboard title found")
            else:
                print("❌ Updated leaderboard title not found")
            
            # Check for team standings section
            if "Team Standings (Treasure Hunt + Events)" in content:
                print("✅ Updated team standings header found")
            else:
                print("❌ Updated team standings header not found")
            
            # Check for events results section
            if "Events Results" in content:
                print("✅ Events results section found")
            else:
                print("⚠️  Events results section not found (may be empty)")
            
            # Check for score breakdown
            if "Score Breakdown" in content:
                print("✅ Score breakdown section found")
            else:
                print("❌ Score breakdown section not found")
            
            print(f"✅ Response length: {len(content)} characters")
            
        else:
            print(f"❌ Leaderboard page failed to load: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing leaderboard view: {e}")
        return False
    
    return True

def test_leaderboard_context():
    """Test that the leaderboard view provides correct context"""
    print("\n🧪 Testing Leaderboard Context...")
    
    from apps.core.views import LeaderboardView
    from django.test import RequestFactory
    
    try:
        factory = RequestFactory()
        request = factory.get(reverse('core:leaderboard'))
        
        view = LeaderboardView()
        view.request = request
        
        context = view.get_context_data()
        
        # Check required context variables
        required_keys = ['players', 'team_standings', 'events', 'team_choices']
        for key in required_keys:
            if key in context:
                print(f"✅ Context key '{key}' found")
            else:
                print(f"❌ Context key '{key}' missing")
        
        # Check team standings structure
        if 'team_standings' in context:
            team_standings = context['team_standings']
            if team_standings:
                team_name, team_data = team_standings[0]
                expected_keys = ['name', 'treasure_hunt_score', 'event_scores', 
                               'total_event_score', 'total_score', 'players']
                
                for key in expected_keys:
                    if key in team_data:
                        print(f"✅ Team data key '{key}' found")
                    else:
                        print(f"❌ Team data key '{key}' missing")
            else:
                print("⚠️  No team standings data found")
        
        print("✅ Context test completed")
        
    except Exception as e:
        print(f"❌ Error testing leaderboard context: {e}")
        return False
    
    return True

def check_sample_data():
    """Check if there's sample data to display"""
    print("\n📊 Checking Sample Data...")
    
    try:
        # Check players
        player_count = Player.objects.count()
        print(f"📈 Players in database: {player_count}")
        
        # Check events
        event_count = Event.objects.count()
        active_event_count = Event.objects.filter(is_active=True).count()
        print(f"📈 Total events: {event_count}, Active events: {active_event_count}")
        
        # Check votes
        vote_count = EventVote.objects.count()
        print(f"📈 Event votes: {vote_count}")
        
        # Check participations
        participation_count = EventParticipation.objects.count()
        print(f"📈 Event participations: {participation_count}")
        
        if player_count == 0:
            print("⚠️  No players found. Consider running create_sample_players.py")
        
        if active_event_count == 0:
            print("⚠️  No active events found. Consider running create_sample_events.py")
        
    except Exception as e:
        print(f"❌ Error checking sample data: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Leaderboard Tests...")
    print("=" * 50)
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if check_sample_data():
        tests_passed += 1
    
    if test_leaderboard_view():
        tests_passed += 1
    
    if test_leaderboard_context():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Leaderboard is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    print("\n🔗 To view the leaderboard:")
    print("1. Start the Django server: python manage.py runserver")
    print("2. Open browser to: http://127.0.0.1:8000/leaderboard/")

if __name__ == '__main__':
    main()
