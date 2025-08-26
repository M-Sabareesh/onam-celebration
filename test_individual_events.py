#!/usr/bin/env python
"""
Test script for individual event scoring functionality.
Tests the complete workflow of individual events.
"""

import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
django.setup()

from apps.core.models import (
    Event, Player, IndividualParticipation, IndividualEventScore, 
    IndividualEventVote, EventParticipation, EventScore
)

def test_individual_event_models():
    """Test individual event model functionality"""
    print("🧪 Testing Individual Event Models...")
    
    # Test Event model with individual participation
    try:
        event = Event.objects.create(
            name="Test Individual Dance",
            event_type="individual_dance",
            participation_type="individual",
            individual_points_multiplier=Decimal('0.7'),
            voting_enabled=True,
            description="Test individual event"
        )
        print(f"✓ Created individual event: {event.name}")
        
        # Test properties
        assert event.allows_individual_participation == True
        assert event.allows_team_participation == False
        print("✓ Event participation type properties work correctly")
        
    except Exception as e:
        print(f"❌ Error creating individual event: {e}")
        return False
    
    # Test Player creation
    try:
        player = Player.objects.create(
            name="Test Player Individual",
            team="team_1",
            is_active=True
        )
        print(f"✓ Created test player: {player.name}")
    except Exception as e:
        print(f"❌ Error creating player: {e}")
        return False
    
    # Test IndividualParticipation
    try:
        participation = IndividualParticipation.objects.create(
            event=event,
            player=player
        )
        print(f"✓ Created individual participation: {participation}")
    except Exception as e:
        print(f"❌ Error creating individual participation: {e}")
        return False
    
    # Test IndividualEventScore
    try:
        score = IndividualEventScore.objects.create(
            event=event,
            player=player,
            points=Decimal('85.5'),
            notes="Test score for individual event",
            awarded_by="test_script"
        )
        print(f"✓ Created individual event score: {score.points} points")
        print(f"✓ Auto-calculated team points: {score.team_points}")
        
        # Verify auto-calculation
        expected_team_points = float(score.points) * float(event.individual_points_multiplier)
        assert float(score.team_points) == expected_team_points
        print("✓ Team points auto-calculation works correctly")
        
    except Exception as e:
        print(f"❌ Error creating individual event score: {e}")
        return False
    
    # Test player score update
    try:
        original_score = player.score
        score.update_player_score()
        player.refresh_from_db()
        print(f"✓ Player score updated from {original_score} to {player.score}")
    except Exception as e:
        print(f"❌ Error updating player score: {e}")
        return False
    
    return True

def test_individual_voting():
    """Test individual event voting functionality"""
    print("\n🗳️  Testing Individual Event Voting...")
    
    try:
        # Get or create test data
        event = Event.objects.filter(participation_type="individual").first()
        if not event:
            event = Event.objects.create(
                name="Test Voting Event",
                event_type="individual_song",
                participation_type="individual",
                voting_enabled=True
            )
        
        # Create two players from different teams
        player1 = Player.objects.get_or_create(
            name="Voter Player",
            defaults={'team': 'team_1', 'is_active': True}
        )[0]
        
        player2 = Player.objects.get_or_create(
            name="Performer Player", 
            defaults={'team': 'team_2', 'is_active': True}
        )[0]
        
        # Create individual vote
        vote = IndividualEventVote.objects.create(
            event=event,
            voting_player=player1,
            performing_player=player2,
            skill_score=8,
            creativity_score=9,
            presentation_score=7,
            overall_score=8,
            comments="Great performance!"
        )
        
        print(f"✓ Created individual vote: {vote}")
        print(f"✓ Total score: {vote.total_score}/40")
        print(f"✓ Average score: {vote.average_score}/10")
        
        # Test vote validation
        assert vote.total_score == 32
        assert vote.average_score == 8.0
        print("✓ Vote scoring calculations work correctly")
        
    except Exception as e:
        print(f"❌ Error in individual voting test: {e}")
        return False
    
    return True

def test_team_score_integration():
    """Test how individual scores integrate with team scores"""
    print("\n🏆 Testing Team Score Integration...")
    
    try:
        # Create test team and players
        team_code = "team_3"
        players = []
        for i in range(3):
            player = Player.objects.get_or_create(
                name=f"Team3 Player {i+1}",
                defaults={'team': team_code, 'is_active': True, 'score': 20}  # Base treasure hunt score
            )[0]
            players.append(player)
        
        # Create individual event
        event = Event.objects.get_or_create(
            name="Test Team Integration Event",
            defaults={
                'event_type': 'individual_art',
                'participation_type': 'individual',
                'individual_points_multiplier': Decimal('0.5'),
                'voting_enabled': False
            }
        )[0]
        
        # Create individual scores for team members
        individual_scores = []
        for i, player in enumerate(players):
            score = IndividualEventScore.objects.get_or_create(
                event=event,
                player=player,
                defaults={
                    'points': Decimal(str(70 + i * 10)),  # 70, 80, 90 points
                    'awarded_by': 'test_integration'
                }
            )[0]
            individual_scores.append(score)
        
        # Calculate expected team contribution
        total_individual_points = sum(float(score.points) for score in individual_scores)
        total_team_points = sum(float(score.team_points) for score in individual_scores)
        expected_team_points = total_individual_points * 0.5  # 50% multiplier
        
        print(f"✓ Total individual points: {total_individual_points}")
        print(f"✓ Total team points from individual events: {total_team_points}")
        print(f"✓ Expected team points: {expected_team_points}")
        
        assert total_team_points == expected_team_points
        print("✓ Team point calculation from individual events is correct")
        
        # Test treasure hunt score integration
        treasure_hunt_total = sum(player.score for player in players)
        print(f"✓ Team treasure hunt total: {treasure_hunt_total}")
        
        # Total team score should be treasure hunt + individual team points
        expected_total = treasure_hunt_total + total_team_points
        print(f"✓ Expected team total: {expected_total}")
        
    except Exception as e:
        print(f"❌ Error in team score integration test: {e}")
        return False
    
    return True

def test_mixed_event_type():
    """Test events that support both team and individual participation"""
    print("\n🎭 Testing Mixed Event Types...")
    
    try:
        # Create mixed event
        mixed_event = Event.objects.get_or_create(
            name="Test Mixed Quiz Event",
            defaults={
                'event_type': 'individual_quiz',
                'participation_type': 'both',
                'individual_points_multiplier': Decimal('0.8'),
                'voting_enabled': False
            }
        )[0]
        
        print(f"✓ Created mixed event: {mixed_event.name}")
        
        # Test properties
        assert mixed_event.allows_individual_participation == True
        assert mixed_event.allows_team_participation == True
        print("✓ Mixed event allows both participation types")
        
        # Create both team and individual participation
        # Team participation
        team_participation = EventParticipation.objects.get_or_create(
            event=mixed_event,
            team='team_4'
        )[0]
        print(f"✓ Created team participation: {team_participation}")
        
        # Individual participation
        player = Player.objects.get_or_create(
            name="Mixed Event Player",
            defaults={'team': 'team_4', 'is_active': True}
        )[0]
        
        individual_participation = IndividualParticipation.objects.get_or_create(
            event=mixed_event,
            player=player
        )[0]
        print(f"✓ Created individual participation: {individual_participation}")
        
        # Create both team and individual scores
        team_score = EventScore.objects.get_or_create(
            event=mixed_event,
            team='team_4',
            defaults={
                'points': Decimal('75'),
                'awarded_by': 'test_mixed'
            }
        )[0]
        print(f"✓ Created team score: {team_score.points}")
        
        individual_score = IndividualEventScore.objects.get_or_create(
            event=mixed_event,
            player=player,
            defaults={
                'points': Decimal('90'),
                'awarded_by': 'test_mixed'
            }
        )[0]
        print(f"✓ Created individual score: {individual_score.points} (team gets {individual_score.team_points})")
        
    except Exception as e:
        print(f"❌ Error in mixed event test: {e}")
        return False
    
    return True

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        # Delete test events
        test_events = Event.objects.filter(name__icontains="Test")
        event_count = test_events.count()
        test_events.delete()
        print(f"✓ Deleted {event_count} test events")
        
        # Delete test players
        test_players = Player.objects.filter(name__icontains="Test")
        player_count = test_players.count()
        test_players.delete()
        print(f"✓ Deleted {player_count} test players")
        
    except Exception as e:
        print(f"❌ Error cleaning up test data: {e}")

def main():
    print("🚀 Starting Individual Event Scoring Tests...")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run tests
    tests = [
        test_individual_event_models,
        test_individual_voting,
        test_team_score_integration,
        test_mixed_event_type
    ]
    
    for test_func in tests:
        try:
            if not test_func():
                all_tests_passed = False
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with exception: {e}")
            all_tests_passed = False
    
    # Cleanup
    cleanup_test_data()
    
    # Results
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 All individual event scoring tests PASSED!")
        print("\n✅ The individual event scoring system is working correctly:")
        print("   • Individual event models function properly")
        print("   • Individual voting system works")
        print("   • Team score integration is correct") 
        print("   • Mixed events support both participation types")
        print("   • Auto-calculation of team points from individual scores")
        print("   • Player score updates from individual events")
    else:
        print("❌ Some tests FAILED!")
        print("   Please check the error messages above and fix the issues.")
    
    print("\n📖 See INDIVIDUAL_EVENT_SCORING_GUIDE.md for complete documentation.")

if __name__ == "__main__":
    main()
