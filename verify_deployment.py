#!/usr/bin/env python
"""
Simple verification script for the admin registration fix
Run this after deployment to verify everything works
"""

import os
import sys

def verify_admin_fix():
    """Verify the admin registration fix"""
    print("🔍 Verifying admin registration fix...")
    
    # Read the admin.py file to verify the fix
    admin_file = "apps/core/admin.py"
    
    if not os.path.exists(admin_file):
        print("❌ admin.py file not found")
        return False
    
    with open(admin_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count occurrences of SimpleEventScore registration
    decorator_count = content.count('@admin.register(SimpleEventScore)')
    manual_count = content.count('admin.site.register(SimpleEventScore')
    
    print(f"📊 Registration count:")
    print(f"   - Decorator registration: {decorator_count}")
    print(f"   - Manual registration: {manual_count}")
    print(f"   - Total: {decorator_count + manual_count}")
    
    if decorator_count == 1 and manual_count == 0:
        print("✅ Admin registration fix verified successfully!")
        print("   - SimpleEventScore is registered exactly once via decorator")
        return True
    elif decorator_count == 0 and manual_count == 1:
        print("✅ Admin registration uses manual method (acceptable)")
        return True
    elif decorator_count + manual_count == 0:
        print("❌ SimpleEventScore is not registered at all!")
        return False
    else:
        print("❌ Multiple registrations detected!")
        print("   This will cause the AlreadyRegistered error")
        return False

def check_file_structure():
    """Check that key files exist"""
    print("\n🔍 Checking file structure...")
    
    required_files = [
        "apps/core/models.py",
        "apps/core/admin.py", 
        "apps/core/views.py",
        "apps/core/urls.py",
        "templates/core/simple_event_scoring_v2.html",
        "manage.py"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    else:
        print("\n✅ All required files present")
        return True

def main():
    """Main verification function"""
    print("🚀 Running deployment verification...\n")
    
    # Change to project directory if needed
    if os.path.exists("onam-celebration"):
        os.chdir("onam-celebration")
    
    results = []
    
    # Run verification checks
    results.append(check_file_structure())
    results.append(verify_admin_fix())
    
    print(f"\n📊 Verification Results: {sum(results)}/{len(results)} checks passed")
    
    if all(results):
        print("\n🎉 Deployment verification successful!")
        print("✅ The admin registration fix should resolve the deployment error")
        print("✅ You can now deploy without the AlreadyRegistered error")
        return 0
    else:
        print("\n⚠️ Some verification checks failed")
        print("Please review the output above before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(main())
