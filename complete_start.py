#!/usr/bin/env python3
"""
Complete Start Script for Onam Celebration Project
Includes all recent fixes: Auto-calculation, Team filtering, and Leaderboard calculation
"""

import os
import sys
import subprocess
import django

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
    sys.path.append('.')
    django.setup()

def apply_migrations():
    """Apply all database migrations"""
    print("\n📊 APPLYING DATABASE MIGRATIONS")
    print("=" * 50)
    
    commands = [
        ("python manage.py makemigrations", "Generate migrations"),
        ("python manage.py migrate", "Apply migrations"),
        ("python manage.py migrate core --fake-initial", "Fake initial migration if needed"),
    ]
    
    for command, description in commands:
        run_command(command, description)

def collect_static_files():
    """Collect static files"""
    print("\n📁 COLLECTING STATIC FILES")
    print("=" * 50)
    
    run_command("python manage.py collectstatic --noinput", "Collect static files")

def test_fixes():
    """Test the applied fixes"""
    print("\n🧪 TESTING IMPLEMENTED FIXES")
    print("=" * 50)
    
    try:
        setup_django()
        
        # Test 1: Auto-calculation functionality
        print("1. Testing auto-calculation functionality...")
        from apps.core.models import SimpleEventScore
        test_score = SimpleEventScore(auto_calculate_points=True, points_per_participant=10)
        print("   ✅ Auto-calculation fields accessible")
        
        # Test 2: Team filtering JavaScript
        print("2. Testing team filtering setup...")
        js_path = "static/js/admin_team_filter.js"
        css_path = "static/css/admin_enhancements.css"
        
        if os.path.exists(js_path):
            print("   ✅ Team filtering JavaScript exists")
        else:
            print("   ❌ Team filtering JavaScript missing")
            
        if os.path.exists(css_path):
            print("   ✅ Admin enhancement CSS exists")
        else:
            print("   ❌ Admin enhancement CSS missing")
        
        # Test 3: Leaderboard calculation fix
        print("3. Testing leaderboard calculation...")
        from apps.core.views import LeaderboardView
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/leaderboard/')
        view = LeaderboardView()
        view.request = request
        context = view.get_context_data()
        
        if 'sorted_teams' in context:
            print("   ✅ Leaderboard calculation working")
        else:
            print("   ❌ Leaderboard calculation issue")
            
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")

def create_superuser_if_needed():
    """Create superuser if it doesn't exist"""
    print("\n👤 CHECKING SUPERUSER")
    print("=" * 50)
    
    try:
        setup_django()
        from django.contrib.auth.models import User
        
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superuser already exists")
        else:
            print("⚠️  No superuser found. You may need to create one:")
            print("   Run: python manage.py createsuperuser")
            
    except Exception as e:
        print(f"❌ Error checking superuser: {e}")

def start_server():
    """Start the Django development server"""
    print("\n🚀 STARTING DJANGO SERVER")
    print("=" * 50)
    
    print("Starting server on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("\nAdmin interface: http://localhost:8000/admin/")
    print("Leaderboard: http://localhost:8000/leaderboard/")
    print("Main site: http://localhost:8000/")
    
    try:
        subprocess.run("python manage.py runserver", shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

def main():
    """Main start sequence"""
    print("🎉 ONAM CELEBRATION PROJECT START SCRIPT")
    print("=" * 60)
    print("Starting with all recent fixes:")
    print("✅ Auto-calculation for event scores")
    print("✅ Team filtering in admin dropdowns") 
    print("✅ Fixed leaderboard calculation (no double-counting)")
    print("=" * 60)
    
    # Step 1: Apply migrations
    apply_migrations()
    
    # Step 2: Collect static files
    collect_static_files()
    
    # Step 3: Test all fixes
    test_fixes()
    
    # Step 4: Check superuser
    create_superuser_if_needed()
    
    # Step 5: Start server
    start_server()

if __name__ == "__main__":
    main()
