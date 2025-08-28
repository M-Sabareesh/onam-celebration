#!/usr/bin/env python
"""
Comprehensive deployment test script
Tests the admin fix and overall system health
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_admin_registration():
    """Test that admin registration works without duplicates"""
    print("🔍 Testing admin registration...")
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
    django.setup()
    
    try:
        from django.contrib import admin
        from apps.core.models import SimpleEventScore
        from apps.core.admin import SimpleEventScoreAdmin
        
        # Check if SimpleEventScore is registered
        registered_models = admin.site._registry
        
        if SimpleEventScore in registered_models:
            admin_class = registered_models[SimpleEventScore]
            print(f"✅ SimpleEventScore registered with {admin_class.__class__.__name__}")
            return True
        else:
            print("❌ SimpleEventScore not registered")
            return False
            
    except Exception as e:
        print(f"❌ Admin registration error: {e}")
        return False

def test_django_check():
    """Test Django system check"""
    print("\n🔍 Running Django system check...")
    
    try:
        from django.core.management.commands.check import Command
        from django.core.management.base import BaseCommand
        from io import StringIO
        import sys
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            execute_from_command_line(['manage.py', 'check'])
            output = captured_output.getvalue()
            sys.stdout = old_stdout
            
            if "System check identified no issues" in output or len(output.strip()) == 0:
                print("✅ Django system check passed")
                return True
            else:
                print(f"⚠️ Django check output: {output}")
                return True  # Non-critical issues are OK
                
        except SystemExit as e:
            sys.stdout = old_stdout
            if e.code == 0:
                print("✅ Django system check passed")
                return True
            else:
                print(f"❌ Django check failed with exit code {e.code}")
                return False
                
    except Exception as e:
        print(f"❌ Django check error: {e}")
        return False

def test_models_import():
    """Test that all models can be imported"""
    print("\n🔍 Testing model imports...")
    
    try:
        from apps.core.models import (
            Question, Choice, Player, Event, EventVote, EventScore,
            TreasureHunt, TreasureHuntSubmission, ImageQuestion,
            TeamConfiguration, IndividualParticipation, 
            IndividualEventScore, IndividualEventVote, SimpleEventScore
        )
        print("✅ All core models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Model import error: {e}")
        return False

def test_admin_import():
    """Test that admin module can be imported"""
    print("\n🔍 Testing admin imports...")
    
    try:
        from apps.core import admin
        print("✅ Core admin module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Admin import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting comprehensive deployment test...\n")
    
    tests = [
        test_models_import,
        test_admin_import,
        test_admin_registration,
        test_django_check,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! Deployment should work.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
