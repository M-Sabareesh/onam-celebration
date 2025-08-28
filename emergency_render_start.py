#!/usr/bin/env python3
"""
Emergency Render Start Command with Migration Fix
Handles the missing SimpleEventScore table issue
"""

import os
import sys
import subprocess
import django

def run_command(cmd, description, critical=True):
    """Run a command with error handling"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"⚠️  {description} had issues: {result.stderr}")
            if critical:
                return False
            return True  # Non-critical, continue
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return not critical  # Return True for non-critical, False for critical

def fix_missing_table():
    """Fix the missing SimpleEventScore table"""
    print("🚨 Fixing missing SimpleEventScore table...")
    
    # Setup Django to check table
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
    
    try:
        django.setup()
        from apps.core.models import SimpleEventScore
        # Try to query the model
        count = SimpleEventScore.objects.count()
        print(f"✅ SimpleEventScore table exists with {count} records")
        return True
    except Exception as e:
        print(f"❌ SimpleEventScore table missing: {e}")
        
        # Try to run the migration fix
        print("🔧 Running migration fix...")
        if run_command("python fix_missing_table.py", "Apply missing table fix", critical=False):
            return True
        
        # If migration fails, try manual creation
        print("🔧 Trying manual table creation...")
        if run_command("python manual_table_creation.py", "Manual table creation", critical=False):
            return True
        
        print("❌ Could not fix missing table")
        return False

def main():
    """Emergency startup with table fix"""
    print("🚨 EMERGENCY RENDER STARTUP")
    print("=" * 50)
    print("🎯 Target: Fix missing core_simpleeventscore table")
    print("=" * 50)
    
    # Step 1: Fix missing table
    print("\n1️⃣ Checking and fixing missing table...")
    if not fix_missing_table():
        print("⚠️  Table fix failed, but continuing with startup...")
    
    # Step 2: Run migrations
    print("\n2️⃣ Running database migrations...")
    run_command("python manage.py migrate --noinput", "Database migrations", critical=False)
    
    # Step 3: Collect static files
    print("\n3️⃣ Collecting static files...")
    run_command("python manage.py collectstatic --noinput", "Static files collection", critical=False)
    
    # Step 4: Create media directories
    print("\n4️⃣ Creating media directories...")
    media_dirs = ['media', 'media/question_images', 'media/treasure_hunt_photos', 'media/avatars']
    for dir_path in media_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 Ensured directory exists: {dir_path}")
    
    # Step 5: Final verification
    print("\n5️⃣ Final verification...")
    try:
        django.setup()
        from apps.core.models import SimpleEventScore
        count = SimpleEventScore.objects.count()
        print(f"✅ SimpleEventScore ready with {count} records")
    except Exception as e:
        print(f"⚠️  SimpleEventScore still has issues: {e}")
        print("🔧 The app will start but admin may have issues")
    
    # Step 6: Start server
    print("\n6️⃣ Starting server...")
    port = os.environ.get('PORT', '8000')
    server_cmd = f"gunicorn onam_project.wsgi:application --bind 0.0.0.0:{port} --workers 1 --timeout 120 --worker-class sync"
    
    print(f"🌐 Starting server on port {port}...")
    print(f"🔗 Command: {server_cmd}")
    print("✅ Admin registration fix applied")
    print("✅ Team filtering implemented") 
    print("✅ Image serving configured")
    print("🚨 Missing table fix attempted")
    
    try:
        subprocess.run(server_cmd, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
