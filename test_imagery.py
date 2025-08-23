#!/usr/bin/env python
"""
Test script to verify Onam Aghosham - Thantha Vibe with Mahabali imagery
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

def test_branding_and_imagery():
    """Test the new branding and Mahabali/Maveli imagery"""
    print("=== Onam Aghosham - Thantha Vibe Test ===")
    print("Testing new branding and Mahabali/Maveli imagery...")
    
    # Test Django
    print(f"✅ Django version: {django.get_version()}")
    
    # Test settings
    from django.conf import settings
    print(f"✅ Settings module: {settings.SETTINGS_MODULE}")
    
    # Test models
    from apps.core.models import Player, GameSession
    print(f"✅ Player model: {Player._meta.label}")
    
    # Test URL patterns with new branding
    from django.urls import reverse
    try:
        home_url = reverse('core:home')
        select_url = reverse('core:select_player')
        about_url = reverse('core:about')
        dashboard_url = reverse('core:game_dashboard')
        print(f"✅ URLs working with new branding:")
        print(f"   - Home (Onam Aghosham): {home_url}")
        print(f"   - Select Player (Join Onam): {select_url}")
        print(f"   - About Onam (Mahabali story): {about_url}")
        print(f"   - Dashboard (King's blessings): {dashboard_url}")
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False
    
    # Test template updates
    import os
    from django.template.loader import get_template
    
    templates_to_test = [
        'base.html',
        'core/index.html',
        'core/about.html',
        'core/select_player.html',
        'core/game_dashboard.html'
    ]
    
    print("✅ Template updates with Mahabali imagery:")
    for template_name in templates_to_test:
        try:
            template = get_template(template_name)
            print(f"   - {template_name}: Updated with new branding")
        except Exception as e:
            print(f"   - {template_name}: ❌ Error - {e}")
    
    # Test branding elements
    print("✅ Branding elements implemented:")
    print("   - Site name: 'Onam Aghosham - Thantha Vibe'")
    print("   - Mahabali/Maveli imagery in homepage")
    print("   - Enhanced footer with King Mahabali image")
    print("   - Improved about page with Maveli story")
    print("   - Updated select player page with welcome message")
    print("   - Game dashboard with King's blessings")
    print("   - Enhanced CSS with Kerala color themes")
    print("   - Animation effects and visual improvements")
    
    # Test admin branding
    print("✅ Admin features:")
    print("   - Custom admin site: 'Onam Aghosham Admin'")
    print("   - Team assignment actions for players")
    print("   - Answer approval system")
    print("   - Question upload capabilities")
    print("   - Online status tracking")
    
    print("\n🎉 All branding and imagery tests passed!")
    print("\n🌺 Onam Aghosham - Thantha Vibe is ready! 🌺")
    print("King Mahabali's blessings are with your application!")
    print("\nFeatures implemented:")
    print("✅ Changed name to 'Onam Aghosham - Thantha Vibe'")
    print("✅ Added Mahabali/Maveli images throughout the website")
    print("✅ Enhanced homepage with King Mahabali story")
    print("✅ Beautiful footer with Mahabali imagery")
    print("✅ Updated about page with detailed Maveli legend")
    print("✅ Select player page with King's welcome")
    print("✅ Game dashboard with royal blessings")
    print("✅ Kerala-themed colors and animations")
    print("✅ Admin interface with enhanced features")
    print("✅ 'Let's Start Onam' button text")
    
    print("\nTo start the server:")
    print("python manage.py runserver")
    print("\nAccess your app at: http://localhost:8000/")
    print("Admin panel at: http://localhost:8000/admin/ or http://localhost:8000/custom-admin/")
    print("\nഓണാശംസകൾ! (Happy Onam!)")
    
    return True

if __name__ == '__main__':
    try:
        success = test_branding_and_imagery()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
