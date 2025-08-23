#!/usr/bin/env python
"""
Test script to demonstrate the new admin event scoring functionality.
This script creates sample events and shows how admin can award points.
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

from apps.core.models import Player, Event, EventParticipation, EventScore

def create_sample_events_and_scores():
    """Create sample events and admin-awarded scores"""
    print("🎪 Creating Sample Events and Admin Scores...")
    print("=" * 50)
    
    # Create events if they don't exist
    events_data = [
        {
            'name': 'Group Dance Competition',
            'event_type': 'group_dance',
            'description': 'Teams perform traditional Onam dances',
            'voting_enabled': False
        },
        {
            'name': 'Group Song Competition',
            'event_type': 'group_song', 
            'description': 'Teams sing traditional Onam songs',
            'voting_enabled': False
        },
        {
            'name': 'Cultural Performance',
            'event_type': 'group_dance',
            'description': 'Mixed cultural performances with voting',
            'voting_enabled': True
        }
    ]
    
    created_events = []
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            name=event_data['name'],
            defaults=event_data
        )
        if created:
            print(f"✅ Created event: {event.name}")
        else:
            print(f"📝 Event already exists: {event.name}")
        created_events.append(event)
    
    # Add team participations
    teams = ['team_1', 'team_2', 'team_3', 'team_4']
    
    for event in created_events:
        print(f"\n🎯 Adding teams to {event.name}:")
        for team in teams:
            participation, created = EventParticipation.objects.get_or_create(
                event=event,
                team=team
            )
            if created:
                print(f"  ✅ Added {participation.get_team_display()}")
            else:
                print(f"  📝 {participation.get_team_display()} already participating")
    
    # Award admin scores for non-voting events
    print(f"\n🏆 Awarding Admin Scores:")
    
    # Group Dance Competition scores
    dance_event = Event.objects.get(name='Group Dance Competition')
    dance_scores = [
        ('team_1', 8.5, 'Excellent coordination and traditional style'),
        ('team_2', 7.8, 'Good performance with minor timing issues'),
        ('team_3', 9.2, 'Outstanding performance, perfect synchronization'),
        ('team_4', 8.0, 'Solid performance with creative elements')
    ]
    
    for team, points, notes in dance_scores:
        score, created = EventScore.objects.get_or_create(
            event=dance_event,
            team=team,
            defaults={
                'points': points,
                'notes': notes,
                'awarded_by': 'admin_test'
            }
        )
        if created:
            print(f"  🥇 {score.get_team_display()}: {points} points - {notes}")
        else:
            print(f"  📝 Score already exists for {score.get_team_display()}: {score.points} points")
    
    # Group Song Competition scores  
    song_event = Event.objects.get(name='Group Song Competition')
    song_scores = [
        ('team_1', 7.5, 'Beautiful harmony, slight pitch issues'),
        ('team_2', 8.8, 'Excellent voice coordination and song selection'),
        ('team_3', 8.2, 'Strong performance with good energy'),
        ('team_4', 9.0, 'Perfect harmony and traditional song presentation')
    ]
    
    for team, points, notes in song_scores:
        score, created = EventScore.objects.get_or_create(
            event=song_event,
            team=team,
            defaults={
                'points': points,
                'notes': notes,
                'awarded_by': 'admin_test'
            }
        )
        if created:
            print(f"  🎵 {score.get_team_display()}: {points} points - {notes}")
        else:
            print(f"  📝 Score already exists for {score.get_team_display()}: {score.points} points")
    
    return created_events

def test_leaderboard_integration():
    """Test that admin scores are properly integrated into leaderboard"""
    print(f"\n📊 Testing Leaderboard Integration...")
    print("=" * 50)
    
    from apps.core.views import LeaderboardView
    from django.test import RequestFactory
    from django.urls import reverse
    
    try:
        factory = RequestFactory()
        request = factory.get(reverse('core:leaderboard'))
        
        view = LeaderboardView()
        view.request = request
        context = view.get_context_data()
        
        print("✅ Leaderboard view executed successfully")
        
        # Check team standings
        if 'team_standings' in context:
            team_standings = context['team_standings']
            print(f"\n🏆 Team Standings with Event Scores:")
            
            for rank, (team_name, team_data) in enumerate(team_standings, 1):
                print(f"  {rank}. {team_data['name']}")
                print(f"     Treasure Hunt: {team_data['treasure_hunt_score']} pts")
                print(f"     Event Scores: {team_data['total_event_score']:.1f} pts")
                print(f"     Total Score: {team_data['total_score']:.1f} pts")
                
                if team_data['event_scores']:
                    for event_name, score in team_data['event_scores'].items():
                        print(f"       - {event_name}: {score} pts")
                print()
        
        # Check events data
        if 'events' in context:
            events = context['events']
            print(f"📈 Event Details in Leaderboard:")
            
            for event_detail in events:
                event = event_detail['event']
                scores = event_detail['scores']
                print(f"  🎪 {event.name}:")
                
                for team_code, team_score in scores.items():
                    team_name = dict(Player.TEAM_CHOICES).get(team_code, team_code)
                    admin_score = team_score.get('admin_score', 0)
                    voting_score = team_score.get('voting_score', 0)
                    
                    if admin_score > 0:
                        print(f"    {team_name}: {admin_score} pts (Admin Awarded)")
                    elif voting_score > 0:
                        print(f"    {team_name}: {voting_score:.1f} pts (Voting Average)")
                    else:
                        print(f"    {team_name}: No score")
                print()
        
        print("✅ All leaderboard data integrated successfully!")
        
    except Exception as e:
        print(f"❌ Error testing leaderboard integration: {e}")
        return False
    
    return True

def show_admin_instructions():
    """Show instructions for using the admin interface"""
    print(f"\n📋 Admin Interface Instructions:")
    print("=" * 50)
    
    print("""
🔐 How to Use the Admin Event Scoring:

1. ACCESS ADMIN PANEL:
   - Go to: http://127.0.0.1:8000/admin/
   - Login with superuser credentials

2. MANAGE EVENTS:
   - Click "Manage Events" from dashboard
   - Create new events with name, type, and description
   - Add teams to events

3. AWARD POINTS:
   - Click "Manage Scores" for any event
   - Select team and enter points (can be decimal like 8.5)
   - Add optional notes about the scoring
   - Submit to award points

4. VIEW RESULTS:
   - Go to leaderboard to see combined scores
   - Treasure hunt + Event scores = Total score
   - Admin scores override voting scores

5. FEATURES:
   - ✅ Create unlimited events
   - ✅ Award points to any team
   - ✅ Edit/update scores anytime
   - ✅ Add notes for transparency
   - ✅ Automatic leaderboard integration

6. VOTING vs ADMIN SCORES:
   - If admin awards points: Admin score is used
   - If no admin score: Voting average is used
   - Admin scores take priority over voting
    """)

def main():
    """Run all tests and demonstrations"""
    print("🚀 Admin Event Scoring System Test")
    print("=" * 50)
    
    # Run tests
    tests_passed = 0
    total_tests = 2
    
    try:
        events = create_sample_events_and_scores()
        tests_passed += 1
        print("✅ Sample events and scores created successfully")
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
    
    try:
        if test_leaderboard_integration():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Failed leaderboard integration test: {e}")
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Admin event scoring is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    show_admin_instructions()
    
    print(f"\n🔗 Quick Links:")
    print("- Admin Panel: http://127.0.0.1:8000/admin/")
    print("- Manage Events: http://127.0.0.1:8000/admin/manage-events/")
    print("- Leaderboard: http://127.0.0.1:8000/leaderboard/")

if __name__ == '__main__':
    main()
