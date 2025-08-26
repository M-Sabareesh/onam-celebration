#!/usr/bin/env python
"""
Clean up duplicate TeamEventParticipation entries
This script removes duplicate team participation records that may have been created
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

def clean_duplicate_participations():
    """Remove duplicate team event participation entries"""
    from apps.core.models import TeamEventParticipation
    from django.db.models import Count
    
    print("🧹 Cleaning duplicate team event participation entries...")
    
    # Find duplicates
    duplicates = (TeamEventParticipation.objects
                 .values('event_score', 'player')
                 .annotate(count=Count('id'))
                 .filter(count__gt=1))
    
    if not duplicates:
        print("✅ No duplicate entries found!")
        return True
    
    print(f"⚠️ Found {len(duplicates)} sets of duplicate entries")
    
    total_deleted = 0
    
    for duplicate in duplicates:
        # Get all entries for this event_score/player combination
        entries = TeamEventParticipation.objects.filter(
            event_score=duplicate['event_score'],
            player=duplicate['player']
        ).order_by('-created_at')  # Keep the most recent one
        
        # Delete all but the first (most recent) entry
        entries_to_delete = entries[1:]
        count = len(entries_to_delete)
        
        if count > 0:
            for entry in entries_to_delete:
                entry.delete()
            
            total_deleted += count
            print(f"   Deleted {count} duplicate entries for event_score {duplicate['event_score']}, player {duplicate['player']}")
    
    print(f"✅ Cleanup complete! Deleted {total_deleted} duplicate entries")
    return True

def verify_cleanup():
    """Verify that cleanup was successful"""
    from apps.core.models import TeamEventParticipation
    from django.db.models import Count
    
    print("\n🔍 Verifying cleanup...")
    
    # Check for remaining duplicates
    duplicates = (TeamEventParticipation.objects
                 .values('event_score', 'player')
                 .annotate(count=Count('id'))
                 .filter(count__gt=1))
    
    if not duplicates:
        print("✅ No duplicate entries remain!")
        total_count = TeamEventParticipation.objects.count()
        print(f"✅ Total participation records: {total_count}")
        return True
    else:
        print(f"⚠️ Still have {len(duplicates)} sets of duplicates")
        return False

def main():
    """Main execution function"""
    print("🧹 Team Event Participation Cleanup")
    print("=" * 50)
    
    # Setup Django
    if not setup_django():
        sys.exit(1)
    
    # Clean duplicates
    if not clean_duplicate_participations():
        print("❌ Cleanup failed")
        sys.exit(1)
    
    # Verify cleanup
    if not verify_cleanup():
        print("❌ Verification failed")
        sys.exit(1)
    
    print("\n🎉 SUCCESS! Team participation cleanup completed!")
    print("\n✅ You can now:")
    print("   - Use the admin interface to add event scores")
    print("   - Select team participants without duplicate errors")
    print("   - View the leaderboard with accurate team scoring")

if __name__ == '__main__':
    main()
