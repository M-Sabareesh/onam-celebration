#!/usr/bin/env python
"""
Quick test to verify Event models are working
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

def quick_test():
    print("=== Testing Event Models ===")
    
    try:
        from apps.core.models import Event, EventParticipation, EventVote
        print("✓ Models imported successfully")
        
        # Test database connection
        from django.db import connection
        cursor = connection.cursor()
        
        # Check if Event table exists
        cursor.execute("SELECT COUNT(*) FROM core_event;")
        event_count = cursor.fetchone()[0]
        print(f"✓ Event table exists with {event_count} records")
        
        # Try to create a test event
        event, created = Event.objects.get_or_create(
            name="Test Event",
            defaults={
                'event_type': 'group_dance',
                'description': 'Test event for verification',
                'is_active': True,
                'voting_enabled': False
            }
        )
        
        if created:
            print("✓ Successfully created test event")
        else:
            print("✓ Test event already exists")
        
        print(f"Event ID: {event.id}, Name: {event.name}")
        
        # Test Event Participation
        participation, created = EventParticipation.objects.get_or_create(
            event=event,
            team='team_1'
        )
        
        if created:
            print("✓ Successfully created test participation")
        else:
            print("✓ Test participation already exists")
        
        print("✅ All Event models are working correctly!")
        
        # Clean up test data
        if event.name == "Test Event":
            event.delete()
            print("✓ Cleaned up test data")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 Events system is ready!")
        print("You can now:")
        print("1. Run: python create_sample_events.py")
        print("2. Start server: python manage.py runserver")
        print("3. Visit: http://127.0.0.1:8000/events/")
    else:
        print("\n❌ Events system needs fixing")
