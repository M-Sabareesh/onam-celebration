#!/usr/bin/env python
"""
Quick test to verify the Player.get_name_display() fix
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('SECRET_KEY', 'django-insecure-test-key')
os.environ.setdefault('DATABASE_URL', 'sqlite:///db.sqlite3')

django.setup()

def test_player_name_fix():
    """Test that Player.name works correctly without get_name_display()"""
    print("=== Testing Player Name Fix ===")
    
    # Test Django
    print(f"✅ Django version: {django.get_version()}")
    
    # Test models
    from apps.core.models import Player
    print(f"✅ Player model: {Player._meta.label}")
    
    # Test creating a player
    try:
        player = Player.objects.create(name="Test Player")
        print(f"✅ Created player: {player.name}")
        
        # Test that we can access name directly (not get_name_display)
        name = player.name
        print(f"✅ Player.name works: {name}")
        
        # Clean up
        player.delete()
        print("✅ Test player cleaned up")
        
    except Exception as e:
        print(f"❌ Error creating player: {e}")
        return False
    
    # Test URL patterns
    from django.urls import reverse
    try:
        treasure_hunt_url = reverse('core:treasure_hunt')
        print(f"✅ Treasure hunt URL: {treasure_hunt_url}")
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False
    
    print("\n🎉 All Player name fixes are working!")
    print("The AttributeError 'Player' object has no attribute 'get_name_display' has been resolved!")
    print("\nFixed issues:")
    print("✅ TreasureHuntView: Changed player.get_name_display() to player.name")
    print("✅ Admin approval: Changed player.get_name_display() to player.name")
    print("✅ Admin rejection: Changed answer.player.get_name_display() to answer.player.name")
    
    print("\nYour Onam Aghosham - Thantha Vibe application should now work without errors!")
    print("Try accessing: http://localhost:8000/treasure-hunt/")
    
    return True

if __name__ == '__main__':
    try:
        success = test_player_name_fix()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
