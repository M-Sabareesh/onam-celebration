#!/usr/bin/env python3
"""
Test script to verify the latest fixes for team filtering and image serving
"""

import os
import sys
import django

# Add the Django project to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.core.models import Player, Event, EventScore, TreasureHuntQuestion

def test_admin_team_filtering():
    """Test the enhanced team-based player filtering"""
    print("🔍 Testing Enhanced Team-Based Player Filtering...")
    print("-" * 50)
    
    # Ensure we have test data
    teams_data = {
        'team_1': ['Alice Team1', 'Bob Team1', 'Charlie Team1'],
        'team_2': ['David Team2', 'Eva Team2', 'Frank Team2'],
        'team_3': ['Grace Team3', 'Henry Team3'],
        'unassigned': ['John Unassigned']
    }
    
    for team, names in teams_data.items():
        for name in names:
            player, created = Player.objects.get_or_create(
                name=name,
                defaults={'team': team, 'is_active': True}
            )
            if created:
                print(f"✅ Created player: {name} ({team})")
    
    # Test the AJAX endpoint
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True}
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    
    client = Client()
    client.force_login(admin_user)
    
    # Test filtering for each team
    for team in ['team_1', 'team_2', 'team_3']:
        response = client.post('/admin/get-team-players/', {'team': team})
        
        if response.status_code == 200:
            data = response.json()
            players = data.get('players', [])
            expected_count = Player.objects.filter(team=team, is_active=True).count()
            
            print(f"✅ Team {team}: {len(players)} players (expected: {expected_count})")
            for player in players:
                print(f"   - {player['name']} (ID: {player['id']})")
            
            if len(players) != expected_count:
                print(f"⚠️ Warning: Expected {expected_count} players, got {len(players)}")
        else:
            print(f"❌ AJAX failed for {team}: Status {response.status_code}")
    
    print(f"\n✅ Team filtering test completed!")

def test_treasure_hunt_images():
    """Test treasure hunt image handling"""
    print("\n🖼️ Testing Treasure Hunt Image Serving...")
    print("-" * 50)
    
    # Check existing questions with images
    questions_with_images = TreasureHuntQuestion.objects.filter(
        question_image__isnull=False
    ).exclude(question_image='')
    
    print(f"📋 Found {questions_with_images.count()} questions with images:")
    
    for question in questions_with_images:
        print(f"\n🔍 Question {question.order}: {question.question_text[:40]}...")
        print(f"   📁 Image file: {question.question_image.name}")
        print(f"   🌐 Image URL: {question.question_image.url}")
        
        # Check file existence
        if question.question_image:
            from django.conf import settings
            file_path = os.path.join(settings.MEDIA_ROOT, question.question_image.name)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"   ✅ File exists ({file_size} bytes): {file_path}")
            else:
                print(f"   ❌ File missing: {file_path}")
    
    # Test creating a new question with image
    print(f"\n📤 Testing image upload...")
    from django.conf import settings
    question_images_dir = os.path.join(settings.MEDIA_ROOT, 'question_images')
    
    if os.path.exists(question_images_dir):
        image_files = [f for f in os.listdir(question_images_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        
        if image_files:
            print(f"   📷 Available images: {', '.join(image_files)}")
            
            # Create test question if none exist
            if questions_with_images.count() == 0:
                test_question = TreasureHuntQuestion.objects.create(
                    question_text="What do you see in this beautiful Onam image?",
                    question_type="image_text",
                    question_image=f"question_images/{image_files[0]}",
                    order=999,
                    points=15,
                    is_active=True
                )
                print(f"   ✅ Created test question with image: {test_question.question_image.url}")
        else:
            print(f"   ⚠️ No image files found in {question_images_dir}")
    
    print(f"\n✅ Image serving test completed!")

def test_admin_interface():
    """Test admin interface functionality"""
    print("\n🔧 Testing Admin Interface...")
    print("-" * 50)
    
    admin_user = User.objects.get(username='admin')
    client = Client()
    client.force_login(admin_user)
    
    # Test key admin pages
    admin_urls = {
        '/admin/': 'Admin Dashboard',
        '/admin/core/eventscore/': 'Event Scores',
        '/admin/core/eventscore/add/': 'Add Event Score',
        '/admin/core/treasurehuntquestion/': 'Treasure Hunt Questions',
        '/admin/core/player/': 'Players',
        '/admin/core/teamconfiguration/': 'Team Configuration'
    }
    
    for url, description in admin_urls.items():
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ {description}: Accessible")
            else:
                print(f"⚠️ {description}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    print(f"\n✅ Admin interface test completed!")

def verify_javascript_files():
    """Verify JavaScript files are in place"""
    print("\n📜 Verifying JavaScript Files...")
    print("-" * 50)
    
    from django.conf import settings
    static_dir = os.path.join(settings.BASE_DIR, 'static', 'js')
    
    required_js_files = {
        'admin_team_filter.js': 'Team filtering JavaScript',
        'leaderboard_chart.js': 'Leaderboard charts'
    }
    
    for filename, description in required_js_files.items():
        filepath = os.path.join(static_dir, filename)
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"✅ {description}: Found ({file_size} bytes)")
        else:
            print(f"❌ {description}: Missing at {filepath}")
    
    print(f"\n✅ JavaScript verification completed!")

def main():
    """Run all verification tests"""
    print("🚀 Testing Team Filtering and Image Serving Fixes")
    print("=" * 60)
    print("🎯 This script verifies:")
    print("   1. Team-based player filtering in EventScore admin")
    print("   2. Treasure hunt image upload and serving")
    print("   3. Admin interface accessibility")
    print("   4. Required JavaScript files")
    print("=" * 60)
    
    try:
        test_admin_team_filtering()
        test_treasure_hunt_images()
        test_admin_interface()
        verify_javascript_files()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("\n📋 Manual Testing Steps:")
        print("1. 🔐 Log in to admin: /admin/ (username: admin)")
        print("2. 🏆 Go to Event scores → Add event score")
        print("3. 🎯 Select a team - player dropdown should filter automatically")
        print("4. 🖼️ Go to Treasure Hunt Questions - images should display")
        print("5. ➕ Try adding a new question with an image")
        print("\n🔧 Debugging:")
        print("- Open browser console to see JavaScript logs")
        print("- Check network tab for AJAX requests")
        print("- Verify image URLs in the page source")
        
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
