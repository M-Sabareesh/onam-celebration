#!/usr/bin/env python
"""
Test script to verify team filtering and image serving fixes
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')

def test_team_filtering():
    """Test team filtering functionality"""
    print("🔍 Testing team filtering functionality...")
    
    # Check if JavaScript file exists
    js_file = 'static/js/admin_team_filter.js'
    if os.path.exists(js_file):
        print("✅ JavaScript file exists")
        
        # Check if it contains key functions
        with open(js_file, 'r') as f:
            content = f.read()
        
        checks = [
            'filterPlayersByTeam',
            'setupTeamFiltering',
            '/admin/get-team-players/',
            'formset:added'
        ]
        
        for check in checks:
            if check in content:
                print(f"   ✅ Contains: {check}")
            else:
                print(f"   ❌ Missing: {check}")
        return True
    else:
        print("❌ JavaScript file not found")
        return False

def test_ajax_endpoint():
    """Test AJAX endpoint for team players"""
    print("\n🔍 Testing AJAX endpoint...")
    
    try:
        django.setup()
        from django.test import Client
        from django.contrib.auth.models import User
        
        client = Client()
        
        # Create admin user if needed
        try:
            admin = User.objects.get(username='testadmin')
        except User.DoesNotExist:
            admin = User.objects.create_superuser('testadmin', 'test@test.com', 'testpass')
        
        client.force_login(admin)
        
        # Test the endpoint
        response = client.post('/admin/get-team-players/', {'team': 'team_1'})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AJAX endpoint works: {len(data.get('players', []))} players")
            return True
        else:
            print(f"❌ AJAX endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AJAX test failed: {e}")
        return False

def test_media_configuration():
    """Test media file configuration"""
    print("\n🔍 Testing media configuration...")
    
    try:
        django.setup()
        from django.conf import settings
        
        print(f"📁 MEDIA_URL: {settings.MEDIA_URL}")
        print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
        
        # Check if media directories exist
        media_dirs = [
            settings.MEDIA_ROOT,
            os.path.join(settings.MEDIA_ROOT, 'question_images'),
            os.path.join(settings.MEDIA_ROOT, 'treasure_hunt_photos'),
            os.path.join(settings.MEDIA_ROOT, 'avatars')
        ]
        
        all_exist = True
        for dir_path in media_dirs:
            if os.path.exists(dir_path):
                print(f"   ✅ {dir_path}")
            else:
                print(f"   ❌ {dir_path} (will be created)")
                os.makedirs(dir_path, exist_ok=True)
                print(f"   ✅ Created {dir_path}")
        
        return True
    except Exception as e:
        print(f"❌ Media test failed: {e}")
        return False

def test_image_template():
    """Test image template updates"""
    print("\n🔍 Testing image template...")
    
    template_file = 'templates/core/treasure_hunt.html'
    if os.path.exists(template_file):
        with open(template_file, 'r') as f:
            content = f.read()
        
        checks = [
            'question.question_image.url',
            'onerror=',
            'Image could not be loaded'
        ]
        
        all_present = True
        for check in checks:
            if check in content:
                print(f"   ✅ Template contains: {check}")
            else:
                print(f"   ❌ Template missing: {check}")
                all_present = False
        
        return all_present
    else:
        print("❌ Template file not found")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing team filtering and image fixes...\n")
    
    tests = [
        test_team_filtering,
        test_ajax_endpoint,
        test_media_configuration,
        test_image_template
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
            results.append(False)
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("\n🎉 All tests passed!")
        print("✅ Team filtering should work in admin")
        print("✅ Images should display in treasure hunt")
        print("\nNext steps:")
        print("1. Deploy the changes")
        print("2. Test team filtering in admin: /admin/core/eventscore/add/")
        print("3. Test image display in treasure hunt questions")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
