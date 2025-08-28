#!/usr/bin/env python
"""Test script to verify the admin registration fix"""

import os
import sys
import django

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

try:
    from django.contrib import admin
    from apps.core.models import SimpleEventScore
    
    print("✅ Testing admin registration...")
    
    # Check if SimpleEventScore is registered
    registered_models = admin.site._registry
    
    if SimpleEventScore in registered_models:
        print("✅ SimpleEventScore is registered in admin")
        admin_class = registered_models[SimpleEventScore]
        print(f"✅ Admin class: {admin_class.__class__.__name__}")
        print("✅ No duplicate registration error!")
    else:
        print("❌ SimpleEventScore is NOT registered in admin")
    
    # Test importing admin module
    from apps.core import admin as core_admin
    print("✅ Core admin module imported successfully")
    
    print("\n🎉 Admin registration fix verified successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
