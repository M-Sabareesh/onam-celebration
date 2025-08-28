#!/usr/bin/env python
"""
Test script to verify both fixes:
1. Team-based player filtering in admin
2. Treasure hunt image serving
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

def test_team_player_filtering():
    """Test that team-based player filtering works"""
    print("🔍 Testing team-based player filtering...")
    
    from apps.core.models import Player, TeamConfiguration
    
    # Check if we have team configurations
    team_configs = TeamConfiguration.objects.all()
    print(f"📊 Found {team_configs.count()} team configurations")
    
    if team_configs.exists():
        for config in team_configs:
            players = Player.objects.filter(team=config.team_code, is_active=True)
            print(f"   - {config.team_name} ({config.team_code}): {players.count()} players")
    
    # Test the AJAX endpoint
    client = Client()
    
    # Create a superuser for testing
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    
    client.force_login(admin_user)
    
    # Test AJAX endpoint
    response = client.post('/admin/get-team-players/', {'team': 'team_1'})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ AJAX endpoint works: {len(data.get('players', []))} players found for team_1")
        return True
    else:
        print(f"❌ AJAX endpoint failed: {response.status_code}")
        return False

def test_treasure_hunt_images():
    """Test that treasure hunt images are configured correctly"""
    print("\n🔍 Testing treasure hunt image configuration...")
    
    from apps.core.models import TreasureHuntQuestion
    from django.conf import settings
    import os
    
    # Check media configuration
    print(f"📁 MEDIA_URL: {settings.MEDIA_URL}")
    print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    # Check if media directory exists
    if os.path.exists(settings.MEDIA_ROOT):
        print("✅ Media directory exists")
        
        # Check question_images subdirectory
        question_images_dir = os.path.join(settings.MEDIA_ROOT, 'question_images')
        if os.path.exists(question_images_dir):
            image_files = os.listdir(question_images_dir)
            print(f"✅ Question images directory exists with {len(image_files)} files")
        else:
            print("📁 Question images directory doesn't exist yet (created on first upload)")
    else:
        print("❌ Media directory doesn't exist")
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        print("✅ Created media directory")
    
    # Check questions with images
    questions_with_images = TreasureHuntQuestion.objects.exclude(question_image='')
    print(f"📊 Found {questions_with_images.count()} questions with images")
    
    for question in questions_with_images:
        if question.question_image:
            image_path = question.question_image.path
            if os.path.exists(image_path):
                print(f"   ✅ {question.order}: Image exists at {image_path}")
            else:
                print(f"   ❌ {question.order}: Image missing at {image_path}")
    
    return True

def test_admin_interface():
    """Test admin interface accessibility"""
    print("\n🔍 Testing admin interface...")
    
    client = Client()
    
    # Test admin URLs
    admin_urls = [
        '/admin/',
        '/custom-admin/',
    ]
    
    for url in admin_urls:
        response = client.get(url, follow=True)
        if response.status_code == 200:
            print(f"✅ {url} accessible")
        else:
            print(f"❌ {url} failed: {response.status_code}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Testing both fixes...\n")
    
    tests = [
        test_team_player_filtering,
        test_treasure_hunt_images,
        test_admin_interface,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! Both fixes should work.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
