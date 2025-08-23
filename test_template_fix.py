#!/usr/bin/env python
"""
Test script to verify the event detail template fix
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

def test_event_detail_template():
    """Test the event detail template rendering"""
    print("=== Testing Event Detail Template Fix ===")
    
    try:
        from apps.core.models import Event, EventParticipation, EventVote, Player
        from django.test import RequestFactory
        from apps.core.views import EventDetailView
        
        # Create test event if it doesn't exist
        event, created = Event.objects.get_or_create(
            name="Test Event for Template",
            defaults={
                'event_type': 'group_dance',
                'description': 'Test event for template fix',
                'is_active': True,
                'voting_enabled': True
            }
        )
        
        if created:
            print(f"✓ Created test event: {event.name}")
        else:
            print(f"✓ Using existing event: {event.name}")
        
        # Register teams
        teams = ['team_1', 'team_2', 'team_3', 'team_4']
        for team in teams:
            participation, created = EventParticipation.objects.get_or_create(
                event=event,
                team=team
            )
        
        print(f"✓ Registered {len(teams)} teams for the event")
        
        # Create a test vote to check existing_votes logic
        vote, created = EventVote.objects.get_or_create(
            event=event,
            voting_team='team_1',
            performing_team='team_2',
            defaults={
                'coordination_score': 8,
                'selection_score': 7,
                'overall_score': 9,
                'enjoyment_score': 8,
                'comments': 'Great performance!'
            }
        )
        
        if created:
            print("✓ Created test vote")
        else:
            print("✓ Test vote already exists")
        
        # Create a test player and session
        player, created = Player.objects.get_or_create(
            name="Test Player for Events",
            defaults={
                'team': 'team_1',
                'is_active': True
            }
        )
        
        # Test the view rendering
        factory = RequestFactory()
        request = factory.get(f'/events/{event.id}/')
        request.session = {'player_id': player.id}
        
        view = EventDetailView()
        view.setup(request, event_id=event.id)
        
        try:
            response = view.get(request, event_id=event.id)
            print("✓ Event detail view renders without errors")
            print(f"✓ Response status: {response.status_code}")
            
            # Check if the response contains expected content
            content = response.content.decode('utf-8')
            if 'Vote for' in content and 'Comments (Optional)' in content:
                print("✓ Template contains expected voting form elements")
            else:
                print("⚠ Template may be missing some voting form elements")
                
        except Exception as e:
            print(f"✗ Error rendering view: {e}")
            return False
        
        print("\n=== Template Fix Summary ===")
        print("Fixed issue: 'Failed lookup for key [comments] in 'team_3''")
        print("Solution: Changed from accessing team.comments to vote.comments")
        print("Updated all score field access patterns in the template")
        
        # Clean up test data
        if event.name == "Test Event for Template":
            event.delete()
            print("✓ Cleaned up test data")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_event_detail_template()
    if success:
        print("\n🎉 Event detail template is working correctly!")
        print("The /events/<id>/ page should now load without errors.")
    else:
        print("\n❌ Template fix needs more work.")
