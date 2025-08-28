#!/usr/bin/env python
"""
Simple verification script to check if files exist and configurations are correct
"""

import os
import sys

def verify_files():
    """Check if all required files exist"""
    print("🔍 Verifying file existence...")
    
    required_files = [
        'static/js/admin_team_filter.js',
        'apps/core/admin.py',
        'apps/core/views.py', 
        'apps/core/urls.py',
        'onam_project/settings/production.py',
        'onam_project/urls.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            all_exist = False
    
    return all_exist

def verify_javascript():
    """Check JavaScript file content"""
    print("\n🔍 Verifying JavaScript content...")
    
    js_file = 'static/js/admin_team_filter.js'
    if os.path.exists(js_file):
        with open(js_file, 'r') as f:
            content = f.read()
        
        checks = [
            'get-team-players',
            'filterPlayersByTeam',
            'django.jQuery',
            'id_team'
        ]
        
        for check in checks:
            if check in content:
                print(f"   ✅ Contains: {check}")
            else:
                print(f"   ❌ Missing: {check}")
        
        return True
    else:
        print("   ❌ JavaScript file not found")
        return False

def verify_url_patterns():
    """Check URL configuration"""
    print("\n🔍 Verifying URL patterns...")
    
    urls_file = 'apps/core/urls.py'
    if os.path.exists(urls_file):
        with open(urls_file, 'r') as f:
            content = f.read()
        
        if 'get-team-players' in content:
            print("   ✅ AJAX endpoint URL configured")
            return True
        else:
            print("   ❌ AJAX endpoint URL missing")
            return False
    else:
        print("   ❌ URLs file not found")
        return False

def verify_media_config():
    """Check media configuration"""
    print("\n🔍 Verifying media configuration...")
    
    prod_settings = 'onam_project/settings/production.py'
    if os.path.exists(prod_settings):
        with open(prod_settings, 'r') as f:
            content = f.read()
        
        checks = [
            'MEDIA_URL',
            'MEDIA_ROOT',
            'WHITENOISE_ROOT'
        ]
        
        all_present = True
        for check in checks:
            if check in content:
                print(f"   ✅ {check} configured")
            else:
                print(f"   ❌ {check} missing")
                all_present = False
        
        return all_present
    else:
        print("   ❌ Production settings not found")
        return False

def main():
    """Run verification"""
    print("🚀 Running verification for both fixes...\n")
    
    tests = [
        verify_files,
        verify_javascript,
        verify_url_patterns,
        verify_media_config
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            results.append(False)
    
    print(f"\n📊 Verification Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("\n🎉 All verifications passed!")
        print("✅ Team filtering should work in admin")
        print("✅ Images should display in treasure hunt")
        print("\nTo deploy:")
        print("1. Commit and push changes")
        print("2. Deploy to production")
        print("3. Test both features in admin interface")
        return 0
    else:
        print("\n⚠️ Some verifications failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
