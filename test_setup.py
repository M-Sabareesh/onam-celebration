#!/usr/bin/env python
"""
Django Onam Project - Setup Test
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

def test_setup():
    """Test Django setup"""
    print("=== Django Onam Project Setup Test ===")
    
    # Test Django
    print(f"✅ Django version: {django.get_version()}")
    
    # Test settings
    from django.conf import settings
    print(f"✅ Settings module: {settings.SETTINGS_MODULE}")
    print(f"✅ Debug mode: {settings.DEBUG}")
    
    # Test database
    from django.db import connection
    print(f"✅ Database: {connection.vendor}")
    
    # Test models
    from apps.core.models import Player, GameSession
    print(f"✅ Player model: {Player._meta.label}")
    print(f"✅ GameSession model: {GameSession._meta.label}")
    
    # Test player names
    print("✅ Available player names:")
    for code, name in Player.PLAYER_NAMES:
        print(f"   - {name} ({code})")
    
    # Test URL patterns
    from django.urls import reverse
    try:
        home_url = reverse('core:home')
        select_url = reverse('core:select_player')
        dashboard_url = reverse('core:game_dashboard')
        print(f"✅ URLs working:")
        print(f"   - Home: {home_url}")
        print(f"   - Select Player: {select_url}")
        print(f"   - Dashboard: {dashboard_url}")
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False
    
    # Test static files
    print(f"✅ Static URL: {settings.STATIC_URL}")
    print(f"✅ Static root: {settings.STATIC_ROOT}")
    
    print("\n🎉 All tests passed! Your Django Onam Project is ready!")
    print("\nTo start the development server:")
    print("python manage.py runserver")
    
    return True

if __name__ == '__main__':
    try:
        success = test_setup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
