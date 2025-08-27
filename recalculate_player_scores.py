#!/usr/bin/env python
"""
Recalculate Player Scores - Team Event Contribution Fix
This script recalculates all player scores to include their contributions from team events
"""

import os
import sys
import django

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
    try:
        django.setup()
        print("✅ Django environment configured")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def recalculate_all_player_scores():
    """Recalculate scores for all players including team event contributions"""
    from apps.core.models import Player, PlayerAnswer, IndividualEventScore, EventScore, TeamEventParticipation
    from django.db.models import Sum
    
    print("🧮 Recalculating all player scores with team event contributions...")
    
    players = Player.objects.all()
    updated_count = 0
    
    for player in players:
        old_score = player.score
        
        # 1. Get treasure hunt score
        treasure_hunt_score = PlayerAnswer.objects.filter(
            player=player, 
            is_correct=True
        ).aggregate(Sum('points_awarded'))['points_awarded__sum'] or 0
        
        # 2. Get individual event scores
        individual_event_score = IndividualEventScore.objects.filter(
            player=player
        ).aggregate(Sum('points'))['points__sum'] or 0
        
        # 3. Get team event contributions (player's share of team events they participated in)
        team_event_total = 0
        for event_score in EventScore.objects.filter(team=player.team):
            participants = event_score.get_participants()
            if participants.filter(player=player).exists() and participants.count() > 0:
                team_event_total += float(event_score.points) / participants.count()
        
        # 4. Calculate new total score
        new_total = treasure_hunt_score + float(individual_event_score) + team_event_total
        
        # 5. Update player score
        player.score = new_total
        player.save(update_fields=['score'])
        
        # 6. Report change
        if abs(old_score - new_total) > 0.01:  # Only report if there's a meaningful change
            print(f"   {player.name} ({player.get_team_display()}): {old_score} → {new_total:.2f}")
            if team_event_total > 0:
                print(f"      ↳ Team event contribution: +{team_event_total:.2f} pts")
            updated_count += 1
        else:
            print(f"   {player.name}: {new_total:.2f} (no change)")
    
    print(f"\n✅ Score recalculation complete!")
    print(f"   📊 Players processed: {players.count()}")
    print(f"   📈 Players with score changes: {updated_count}")
    
    return True

def show_team_event_breakdown():
    """Show breakdown of team event contributions"""
    from apps.core.models import EventScore, TeamEventParticipation
    
    print("\n📋 Team Event Contribution Breakdown:")
    print("=" * 50)
    
    for event_score in EventScore.objects.all().order_by('event__name'):
        participants = event_score.get_participants()
        if participants.exists():
            individual_share = float(event_score.points) / participants.count()
            print(f"\n🏆 {event_score.event.name} ({event_score.get_team_display()})")
            print(f"   Total Points: {event_score.points}")
            print(f"   Participants: {participants.count()}")
            print(f"   Points per participant: {individual_share:.2f}")
            print(f"   Participating players:")
            for participation in participants:
                print(f"      - {participation.player.name}")

def main():
    """Main execution function"""
    print("🧮 Player Score Recalculation - Team Event Fix")
    print("=" * 60)
    print("This script fixes player scores to include team event contributions")
    print()
    
    # Setup Django
    if not setup_django():
        sys.exit(1)
    
    # Show current team event breakdown
    show_team_event_breakdown()
    
    # Recalculate all scores
    if not recalculate_all_player_scores():
        print("❌ Score recalculation failed")
        sys.exit(1)
    
    print("\n🎉 SUCCESS! Player scores now include team event contributions!")
    print("\n✅ What's fixed:")
    print("   - Players now get individual credit for team event participation")
    print("   - Team event points are distributed among participating players")
    print("   - Individual player scores reflect all contributions")
    print("   - Leaderboard will show accurate individual rankings")
    
    print("\n🔄 Next steps:")
    print("   1. Check the leaderboard to see updated individual scores")
    print("   2. Verify team totals remain the same")
    print("   3. Admin can continue scoring events normally")

if __name__ == '__main__':
    main()
