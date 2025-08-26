#!/usr/bin/env python
"""
Script to demonstrate team event participation tracking system.
Shows how individual player participation in team events affects scoring.
"""

import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
django.setup()

from apps.core.models import Event, Player, EventScore, TeamEventParticipation, EventParticipation

def create_sample_team_events():
    """Create sample team events for testing participation tracking"""
    
    team_events = [
        {
            'name': 'Group Thiruvathira Dance',
            'event_type': 'group_dance',
            'participation_type': 'team',
            'description': 'Traditional Thiruvathira dance - points based on participant count',
            'voting_enabled': False
        },
        {
            'name': 'Team Malayalam Song',
            'event_type': 'group_song', 
            'participation_type': 'team',
            'description': 'Team song performance - bonus for more participants',
            'voting_enabled': True
        },
        {
            'name': 'Group Pookalam Competition',
            'event_type': 'group_dance',  # Using available choice
            'participation_type': 'team',
            'description': 'Team flower carpet creation - each participant adds value',
            'voting_enabled': False
        }
    ]
    
    created_events = []
    for event_data in team_events:
        event, created = Event.objects.get_or_create(
            name=event_data['name'],
            defaults=event_data
        )
        if created:
            print(f"✓ Created team event: {event.name}")
        else:
            print(f"• Event already exists: {event.name}")
        created_events.append(event)
    
    return created_events

def create_sample_team_scores_with_participation(events):
    """Create event scores with participation tracking"""
    
    scores_created = []
    
    for event in events:
        print(f"\n🎭 Setting up participation for: {event.name}")
        
        # Register teams for the event
        teams_to_register = ['team_1', 'team_2', 'team_3']
        
        for team_code in teams_to_register:
            # Register team participation
            team_participation, created = EventParticipation.objects.get_or_create(
                event=event,
                team=team_code
            )
            if created:
                print(f"  ✓ Registered {dict(Player.TEAM_CHOICES)[team_code]} for {event.name}")
            
            # Create event score with participation tracking
            event_score, created = EventScore.objects.get_or_create(
                event=event,
                team=team_code,
                defaults={
                    'points_per_participant': Decimal('10.0'),  # 10 points per participant
                    'auto_calculate_points': True,
                    'awarded_by': 'sample_script',
                    'notes': f'Auto-calculated based on participant count for {event.name}'
                }
            )
            
            if created:
                print(f"  ✓ Created score tracking for {dict(Player.TEAM_CHOICES)[team_code]}")
                scores_created.append(event_score)
            
            # Get team players and create participation records
            team_players = Player.objects.filter(team=team_code, is_active=True)
            
            if team_players.exists():
                print(f"    📋 Team members for {dict(Player.TEAM_CHOICES)[team_code]}:")
                
                # Simulate different participation scenarios
                import random
                participation_rate = random.uniform(0.6, 1.0)  # 60-100% participation
                participants_count = max(1, int(len(team_players) * participation_rate))
                
                participants = random.sample(list(team_players), participants_count)
                
                for i, player in enumerate(team_players):
                    is_participating = player in participants
                    
                    participation, created = TeamEventParticipation.objects.get_or_create(
                        event_score=event_score,
                        player=player,
                        defaults={
                            'participated': is_participating,
                            'notes': f'Participation record for {event.name}'
                        }
                    )
                    
                    status = "✓ Participating" if is_participating else "✗ Not participating"
                    print(f"      {status}: {player.name}")
                
                # Recalculate points based on actual participation
                event_score.save()  # This triggers auto-calculation
                print(f"    🏆 Final score: {event_score.points} points ({event_score.participant_count} participants × {event_score.points_per_participant} pts each)")
            
            else:
                print(f"    ❌ No active players found for {dict(Player.TEAM_CHOICES)[team_code]}")
    
    return scores_created

def demonstrate_manual_vs_auto_calculation():
    """Show difference between manual and auto-calculated scoring"""
    
    print(f"\n📊 Manual vs Auto-Calculation Demo")
    print("=" * 50)
    
    # Get a sample event
    event = Event.objects.filter(participation_type='team').first()
    if not event:
        print("❌ No team events found")
        return
    
    team_code = 'team_1'
    team_name = dict(Player.TEAM_CHOICES)[team_code]
    
    # Create manual score
    manual_score, created = EventScore.objects.get_or_create(
        event=event,
        team=team_code,
        defaults={
            'points': Decimal('75.0'),  # Fixed 75 points
            'auto_calculate_points': False,
            'awarded_by': 'manual_demo',
            'notes': 'Manually assigned score - not based on participation'
        }
    )
    
    print(f"📝 Manual Scoring Example:")
    print(f"   Event: {event.name}")
    print(f"   Team: {team_name}")
    print(f"   Points: {manual_score.points} (fixed)")
    print(f"   Participants: {manual_score.participant_count} (doesn't affect score)")
    
    # Create auto-calculated score for comparison
    auto_event = Event.objects.create(
        name="Demo Auto-Calc Event",
        event_type="group_dance",
        participation_type="team",
        description="Demo event for auto-calculation"
    )
    
    auto_score = EventScore.objects.create(
        event=auto_event,
        team=team_code,
        points_per_participant=Decimal('12.0'),
        auto_calculate_points=True,
        awarded_by='auto_demo'
    )
    
    # Add some participants
    team_players = Player.objects.filter(team=team_code, is_active=True)[:3]
    for player in team_players:
        TeamEventParticipation.objects.create(
            event_score=auto_score,
            player=player,
            participated=True
        )
    
    # Trigger recalculation
    auto_score.save()
    
    print(f"\n🤖 Auto-Calculation Example:")
    print(f"   Event: {auto_event.name}")
    print(f"   Team: {team_name}")
    print(f"   Points per participant: {auto_score.points_per_participant}")
    print(f"   Participants: {auto_score.participant_count}")
    print(f"   Total points: {auto_score.points} (calculated: {auto_score.participant_count} × {auto_score.points_per_participant})")
    
    # Cleanup demo event
    auto_event.delete()

def show_participation_summary():
    """Show summary of all team event participation"""
    
    print(f"\n📈 Team Event Participation Summary")
    print("=" * 60)
    
    team_events = Event.objects.filter(participation_type__in=['team', 'both'])
    
    for event in team_events:
        print(f"\n🎭 {event.name}")
        
        event_scores = EventScore.objects.filter(event=event)
        
        if not event_scores.exists():
            print("   No scores recorded yet")
            continue
        
        for score in event_scores:
            team_name = dict(Player.TEAM_CHOICES)[score.team]
            calc_type = "Auto" if score.auto_calculate_points else "Manual"
            
            print(f"   📊 {team_name}: {score.points} pts ({calc_type})")
            
            if score.auto_calculate_points:
                print(f"      👥 Participants: {score.participant_count}")
                participants = score.get_participants()
                if participants:
                    participant_names = [p.player.name for p in participants]
                    print(f"      📝 Players: {', '.join(participant_names)}")
            
            if hasattr(score, 'participations'):
                total_eligible = score.participations.count()
                total_participated = score.participations.filter(participated=True).count()
                if total_eligible > 0:
                    participation_rate = (total_participated / total_eligible) * 100
                    print(f"      📈 Participation rate: {participation_rate:.1f}% ({total_participated}/{total_eligible})")

def main():
    print("🎪 Team Event Participation System Demo")
    print("=" * 60)
    
    # Create team events
    events = create_sample_team_events()
    print(f"\n📅 Created/verified {len(events)} team events")
    
    # Create scores with participation tracking
    scores = create_sample_team_scores_with_participation(events)
    print(f"\n🏆 Created/verified {len(scores)} event scores with participation tracking")
    
    # Demonstrate different calculation methods
    demonstrate_manual_vs_auto_calculation()
    
    # Show participation summary
    show_participation_summary()
    
    print("\n" + "=" * 60)
    print("🎉 Team Event Participation Demo Complete!")
    print("\n📋 Key Features Demonstrated:")
    print("   ✓ Individual player participation tracking in team events")
    print("   ✓ Auto-calculation of points based on participant count") 
    print("   ✓ Manual scoring option (fixed points regardless of participants)")
    print("   ✓ Participation rate tracking and reporting")
    print("   ✓ Flexible points-per-participant system")
    
    print("\n🔗 Admin Interface:")
    print("   • Use 'Event Scores' to create team event scores")
    print("   • Check participant boxes for players who participated")
    print("   • Choose auto-calculation or manual point assignment") 
    print("   • View participation rates and team performance")
    
    print("\n📖 See admin interface for detailed participant management!")

if __name__ == "__main__":
    main()
