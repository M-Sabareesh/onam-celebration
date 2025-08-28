#!/usr/bin/env python3
"""
Test script for verifying auto-calculation and team filtering fixes
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
sys.path.append('.')
django.setup()

from apps.core.models import Player, Event, SimpleEventScore, EventScore, TeamEventParticipation
from django.contrib.auth.models import User

def test_auto_calculation():
    """Test the auto-calculation functionality"""
    print("=" * 50)
    print("Testing Auto-Calculation Functionality")
    print("=" * 50)
    
    try:
        # Create test event if it doesn't exist
        event, created = Event.objects.get_or_create(
            name="Test Auto-Calc Event",
            defaults={
                'description': 'Test event for auto-calculation',
                'event_type': 'team',
                'participation_type': 'team'
            }
        )
        if created:
            print(f"✅ Created test event: {event.name}")
        else:
            print(f"✅ Using existing test event: {event.name}")
        
        # Test SimpleEventScore auto-calculation
        print("\n1. Testing SimpleEventScore auto-calculation...")
        
        # Create a team event with auto-calculation
        simple_score = SimpleEventScore.objects.create(
            event=event,
            team='team_1',
            event_type='team',
            auto_calculate_points=True,
            points_per_participant=10
        )
        
        team_1_players = Player.objects.filter(team='team_1', is_active=True)
        expected_points = len(team_1_players) * 10
        
        print(f"   Team 1 active players: {len(team_1_players)}")
        print(f"   Points per participant: 10")
        print(f"   Expected total points: {expected_points}")
        print(f"   Actual points: {simple_score.points}")
        
        if float(simple_score.points) == expected_points:
            print("   ✅ Auto-calculation working correctly!")
        else:
            print("   ❌ Auto-calculation failed!")
        
        # Test hybrid event auto-calculation
        print("\n2. Testing hybrid event auto-calculation...")
        
        hybrid_score = SimpleEventScore.objects.create(
            event=event,
            team='team_2',
            event_type='hybrid',
            auto_calculate_points=True,
            points_per_participant=15
        )
        
        # Add some participants
        team_2_players = Player.objects.filter(team='team_2', is_active=True)[:3]
        for player in team_2_players:
            hybrid_score.participants.add(player)
        
        # Save to trigger calculation
        hybrid_score.save()
        
        expected_hybrid_points = len(team_2_players) * 15
        print(f"   Hybrid participants: {len(team_2_players)}")
        print(f"   Points per participant: 15")
        print(f"   Expected total points: {expected_hybrid_points}")
        print(f"   Actual points: {hybrid_score.points}")
        
        if float(hybrid_score.points) == expected_hybrid_points:
            print("   ✅ Hybrid auto-calculation working correctly!")
        else:
            print("   ❌ Hybrid auto-calculation failed!")
        
        print("\n3. Testing EventScore auto-calculation...")
        
        # Test EventScore auto-calculation
        event_score = EventScore.objects.create(
            event=event,
            team='team_3',
            auto_calculate_points=True,
            points_per_participant=20
        )
        
        team_3_players = Player.objects.filter(team='team_3', is_active=True)
        expected_event_points = len(team_3_players) * 20
        
        print(f"   Team 3 active players: {len(team_3_players)}")
        print(f"   Points per participant: 20")
        print(f"   Expected total points: {expected_event_points}")
        print(f"   Actual points: {event_score.points}")
        
        if float(event_score.points) == expected_event_points:
            print("   ✅ EventScore auto-calculation working correctly!")
        else:
            print("   ❌ EventScore auto-calculation failed!")
        
    except Exception as e:
        print(f"❌ Error during auto-calculation test: {e}")
        import traceback
        traceback.print_exc()

def test_team_filtering():
    """Test the team filtering functionality"""
    print("\n" + "=" * 50)
    print("Testing Team Filtering Setup")
    print("=" * 50)
    
    try:
        # Check if we have players in different teams
        teams_with_players = {}
        for team_code, team_name in Player.TEAM_CHOICES:
            player_count = Player.objects.filter(team=team_code, is_active=True).count()
            teams_with_players[team_code] = player_count
            print(f"   {team_name}: {player_count} active players")
        
        # Check if JavaScript file exists
        js_path = "static/js/admin_team_filter.js"
        if os.path.exists(js_path):
            print(f"✅ JavaScript file exists: {js_path}")
        else:
            print(f"❌ JavaScript file missing: {js_path}")
        
        # Check if CSS file exists
        css_path = "static/css/admin_enhancements.css"
        if os.path.exists(css_path):
            print(f"✅ CSS file exists: {css_path}")
        else:
            print(f"❌ CSS file missing: {css_path}")
        
        # Check if AJAX endpoint is accessible
        from apps.core.views import get_team_players
        print("✅ AJAX endpoint function exists")
        
    except Exception as e:
        print(f"❌ Error during team filtering test: {e}")

def test_database_integrity():
    """Test database integrity and migration status"""
    print("\n" + "=" * 50)
    print("Testing Database Integrity")
    print("=" * 50)
    
    try:
        # Check if SimpleEventScore has the new fields
        from django.db import connection
        cursor = connection.cursor()
        
        cursor.execute("PRAGMA table_info(core_simpleeventscore)")
        columns = [row[1] for row in cursor.fetchall()]
        
        required_columns = ['auto_calculate_points', 'points_per_participant']
        for col in required_columns:
            if col in columns:
                print(f"✅ Column exists: {col}")
            else:
                print(f"❌ Column missing: {col}")
        
        # Test creating a SimpleEventScore with new fields
        test_event, _ = Event.objects.get_or_create(
            name="Test DB Event",
            defaults={'description': 'Test event', 'event_type': 'team'}
        )
        
        test_score = SimpleEventScore(
            event=test_event,
            team='team_1',
            auto_calculate_points=True,
            points_per_participant=5
        )
        test_score.save()
        print("✅ Can create SimpleEventScore with new fields")
        
        # Clean up
        test_score.delete()
        
    except Exception as e:
        print(f"❌ Database integrity test failed: {e}")

def main():
    """Run all tests"""
    print("🔧 Testing Auto-Calculation and Team Filtering Fixes")
    print("=" * 60)
    
    test_database_integrity()
    test_auto_calculation()
    test_team_filtering()
    
    print("\n" + "=" * 60)
    print("✅ Testing completed!")
    print("\nNext steps:")
    print("1. Run migration: python manage.py migrate")
    print("2. Collect static files: python manage.py collectstatic")
    print("3. Test in admin interface:")
    print("   - Go to Admin > Simple Event Scores")
    print("   - Create new score with auto-calculation enabled")
    print("   - Verify team filtering in participants dropdown")

if __name__ == "__main__":
    main()
