#!/usr/bin/env python
"""
Script to create sample individual and team events for testing the Onam celebration system.
This demonstrates the individual event scoring feature.
"""

import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
django.setup()

from apps.core.models import Event, Player, IndividualParticipation, IndividualEventScore

def create_sample_events():
    """Create sample events with individual and team participation"""
    
    # Individual events
    individual_events = [
        {
            'name': 'Individual Classical Dance',
            'event_type': 'individual_dance',
            'participation_type': 'individual',
            'description': 'Individual classical Kerala dance performance',
            'individual_points_multiplier': Decimal('0.5'),  # Individual points contribute 50% to team
            'voting_enabled': True
        },
        {
            'name': 'Solo Song Competition',
            'event_type': 'individual_song',
            'participation_type': 'individual',
            'description': 'Individual Malayalam song performance',
            'individual_points_multiplier': Decimal('0.6'),  # Individual points contribute 60% to team
            'voting_enabled': True
        },
        {
            'name': 'Individual Art Contest',
            'event_type': 'individual_art',
            'participation_type': 'individual',
            'description': 'Individual Onam-themed art creation',
            'individual_points_multiplier': Decimal('0.4'),  # Individual points contribute 40% to team
            'voting_enabled': False
        },
    ]
    
    # Team events
    team_events = [
        {
            'name': 'Group Thiruvathira Dance',
            'event_type': 'group_dance',
            'participation_type': 'team',
            'description': 'Traditional Thiruvathira group dance',
            'voting_enabled': True
        },
        {
            'name': 'Team Malayalam Song',
            'event_type': 'group_song',
            'participation_type': 'team',
            'description': 'Team Malayalam song performance',
            'voting_enabled': True
        },
    ]
    
    # Mixed events (both team and individual)
    mixed_events = [
        {
            'name': 'Onam Quiz Championship',
            'event_type': 'individual_quiz',
            'participation_type': 'both',
            'description': 'Quiz about Onam traditions - individual participation, team contribution',
            'individual_points_multiplier': Decimal('0.8'),  # Individual points contribute 80% to team
            'voting_enabled': False
        },
    ]
    
    all_events = individual_events + team_events + mixed_events
    
    created_events = []
    for event_data in all_events:
        event, created = Event.objects.get_or_create(
            name=event_data['name'],
            defaults=event_data
        )
        if created:
            print(f"✓ Created event: {event.name} ({event.get_participation_type_display()})")
        else:
            print(f"• Event already exists: {event.name}")
        created_events.append(event)
    
    return created_events

def create_sample_individual_participations(events):
    """Create sample individual participations"""
    
    # Get some active players
    players = list(Player.objects.filter(is_active=True)[:8])
    
    if not players:
        print("❌ No active players found. Please create some players first.")
        return []
    
    individual_events = [e for e in events if e.allows_individual_participation]
    
    participations = []
    for event in individual_events:
        # Randomly assign 3-5 players to each individual event
        import random
        participants = random.sample(players, min(len(players), random.randint(3, 5)))
        
        for player in participants:
            participation, created = IndividualParticipation.objects.get_or_create(
                event=event,
                player=player
            )
            if created:
                print(f"✓ {player.name} registered for {event.name}")
                participations.append(participation)
            else:
                print(f"• {player.name} already registered for {event.name}")
    
    return participations

def create_sample_individual_scores(events):
    """Create sample individual event scores"""
    
    individual_events = [e for e in events if e.allows_individual_participation]
    scores_created = []
    
    for event in individual_events:
        participants = IndividualParticipation.objects.filter(event=event)
        
        for participation in participants:
            # Generate realistic scores (1-100 points)
            import random
            points = random.randint(60, 100)
            
            score, created = IndividualEventScore.objects.get_or_create(
                event=event,
                player=participation.player,
                defaults={
                    'points': Decimal(str(points)),
                    'notes': f'Sample score for {event.name}',
                    'awarded_by': 'admin_script'
                }
            )
            
            if created:
                print(f"✓ Awarded {points} points to {participation.player.name} for {event.name}")
                print(f"   Team contribution: {score.team_points} points to {participation.player.get_team_display()}")
                scores_created.append(score)
            else:
                print(f"• Score already exists for {participation.player.name} in {event.name}")
    
    return scores_created

def main():
    print("🎭 Creating sample individual and team events for Onam celebration...")
    print("=" * 60)
    
    # Create events
    events = create_sample_events()
    print(f"\n📅 {len(events)} events processed")
    
    # Create individual participations
    print("\n👥 Creating individual participations...")
    participations = create_sample_individual_participations(events)
    print(f"📝 {len(participations)} individual participations created")
    
    # Create sample scores
    print("\n🏆 Creating sample individual event scores...")
    scores = create_sample_individual_scores(events)
    print(f"📊 {len(scores)} individual scores created")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Sample individual events setup complete!")
    print("\n📋 Summary:")
    
    individual_events = Event.objects.filter(participation_type__in=['individual', 'both'])
    team_events = Event.objects.filter(participation_type__in=['team', 'both'])
    
    print(f"   • Individual events: {individual_events.count()}")
    print(f"   • Team events: {team_events.count()}")
    print(f"   • Total participations: {IndividualParticipation.objects.count()}")
    print(f"   • Total individual scores: {IndividualEventScore.objects.count()}")
    
    print("\n🔗 Next steps:")
    print("   1. Access admin panel to manage individual event scores")
    print("   2. Check leaderboard to see team and individual rankings")
    print("   3. Add more players and events as needed")
    print("   4. Enable voting for events if desired")

if __name__ == "__main__":
    main()
