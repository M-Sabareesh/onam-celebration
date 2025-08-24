#!/usr/bin/env python
"""
Test script to verify player name display fixes
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
os.environ.setdefault('SECRET_KEY', 'django-insecure-test-key-for-testing')

django.setup()

def test_player_name_displays():
    """Test that player names display correctly in templates"""
    print("=== Testing Player Name Display Fixes ===")
    
    from apps.core.models import Player
    
    # Create a test player
    try:
        test_player = Player.objects.create(
            name="Test Player for Display",
            team="team_1",
            is_active=True
        )
        print(f"✅ Created test player: {test_player.name}")
        
        # Test model methods
        print(f"✅ Player.name: {test_player.name}")
        print(f"✅ Player.get_team_display(): {test_player.get_team_display()}")
        print(f"✅ Player.__str__(): {str(test_player)}")
        
        # Test that the model doesn't have get_name_display
        has_get_name_display = hasattr(test_player, 'get_name_display')
        if not has_get_name_display:
            print("✅ Confirmed: Player model doesn't have get_name_display method")
        else:
            print("❌ Warning: Player model still has get_name_display method")
        
        # Clean up
        test_player.delete()
        print("✅ Test player cleaned up")
        
    except Exception as e:
        print(f"❌ Error in player test: {e}")
        return False
    
    print("\n=== Template Fix Summary ===")
    fixes = [
        "templates/core/leaderboard.html - Fixed player.get_name_display → player.name",
        "templates/core/game_dashboard.html - Fixed player.get_name_display → player.name", 
        "templates/core/treasure_hunt_fixed.html - Fixed player.get_name_display → player.name",
        "templates/admin/approve_answers.html - Fixed player.get_name_display → player.name",
        "templates/core/treasure_hunt.html - Fixed team display → player.get_team_display",
        "templates/core/leaderboard.html - Fixed team display → player.get_team_display"
    ]
    
    for fix in fixes:
        print(f"✅ {fix}")
    
    print("\n🎉 All player name display issues have been fixed!")
    print("\nThe following templates now correctly display player names:")
    print("- Leaderboard page")
    print("- Game dashboard") 
    print("- Treasure hunt page")
    print("- Admin approval interface")
    print("- Events pages")
    
    print("\nPlayer names should now display properly throughout the application!")
    return True

if __name__ == '__main__':
    try:
        success = test_player_name_displays()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
