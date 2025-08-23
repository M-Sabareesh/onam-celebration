#!/usr/bin/env python
"""
Script to create sample events for testing the voting system
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

from apps.core.models import Event, EventParticipation, Player

def create_sample_events():
    """Create sample events for testing"""
    print("=== Creating Sample Events ===")
    
    # Create Group Dance Event
    dance_event, created = Event.objects.get_or_create(
        name="Traditional Onam Dance Competition",
        event_type='group_dance',
        defaults={
            'description': 'Teams perform traditional Kerala dances like Thiruvathira and compete for the best performance.',
            'is_active': True,
            'voting_enabled': True
        }
    )
    
    if created:
        print(f"✓ Created dance event: {dance_event.name}")
    else:
        print(f"✓ Dance event already exists: {dance_event.name}")
    
    # Create Group Song Event  
    song_event, created = Event.objects.get_or_create(
        name="Onam Song Competition",
        event_type='group_song',
        defaults={
            'description': 'Teams sing traditional Malayalam songs and Onam songs to celebrate the festival.',
            'is_active': True,
            'voting_enabled': True
        }
    )
    
    if created:
        print(f"✓ Created song event: {song_event.name}")
    else:
        print(f"✓ Song event already exists: {song_event.name}")
    
    print(f"\n=== Setting up Team Participation ===")
    
    # Register all teams for both events
    events = [dance_event, song_event]
    teams = ['team_1', 'team_2', 'team_3', 'team_4']
    
    for event in events:
        for team in teams:
            participation, created = EventParticipation.objects.get_or_create(
                event=event,
                team=team
            )
            
            if created:
                print(f"✓ Registered {team} for {event.name}")
            else:
                print(f"✓ {team} already registered for {event.name}")
    
    print(f"\n=== Events Setup Complete ===")
    print(f"Created {Event.objects.count()} events")
    print(f"Created {EventParticipation.objects.count()} team participations")
    
    print(f"\n=== How to Test ===")
    print("1. Run the Django server: python manage.py runserver")
    print("2. Go to: http://127.0.0.1:8000/events/")
    print("3. Select a player and ensure they're assigned to a team")
    print("4. Vote for other teams' performances")
    print("5. View real-time scores and leaderboard")
    
    print(f"\n=== Admin Access ===")
    print("- Events: http://127.0.0.1:8000/admin/core/event/")
    print("- Team Participation: http://127.0.0.1:8000/admin/core/eventparticipation/")
    print("- Votes: http://127.0.0.1:8000/admin/core/eventvote/")
    
    print(f"\n=== Sample Teams for Testing ===")
    teams_info = {
        'team_1': 'Team 1',
        'team_2': 'Team 2', 
        'team_3': 'Team 3',
        'team_4': 'Team 4'
    }
    
    for team_code, team_name in teams_info.items():
        players_count = Player.objects.filter(team=team_code).count()
        print(f"- {team_name}: {players_count} players")
    
    unassigned_count = Player.objects.filter(team='unassigned').count()
    print(f"- Unassigned: {unassigned_count} players")
    
    if unassigned_count > 0:
        print(f"\n💡 Tip: Assign unassigned players to teams through the admin interface for better testing")

if __name__ == "__main__":
    create_sample_events()
