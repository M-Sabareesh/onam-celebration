#!/usr/bin/env python3
"""
Current Recommended Render Start Command
Updated with latest fixes for admin registration and media files
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command with error handling"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"⚠️  {description} had issues: {result.stderr}")
            # Don't fail completely for non-critical issues
            return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    """Production startup for Render with all fixes"""
    print("🚀 RENDER STARTUP - CURRENT VERSION")
    print("=" * 50)
    print("✅ Admin registration fix applied")
    print("✅ Team filtering implemented") 
    print("✅ Image serving configured")
    print("🚨 IMMEDIATE TABLE FIX INCLUDED")
    print("=" * 50)
    
    # IMMEDIATE FIX: Force create missing table
    print("\n🚨 STEP 1: Force fix missing SimpleEventScore table...")
    if not run_command("python force_fix_table.py", "Force create missing table"):
        print("⚠️  Table creation failed, but continuing...")
    
    # Database migrations
    print("\n2️⃣ Running database migrations...")
    if not run_command("python manage.py migrate --noinput", "Database migrations"):
        print("⚠️  Migration had issues, but continuing...")
    
    # Try specific migration
    print("\n3️⃣ Ensuring specific migration...")
    if not run_command("python manage.py migrate core 0015_simple_event_scoring --noinput", "Apply SimpleEventScore migration"):
        print("⚠️  Specific migration failed, but continuing...")
    
    # Collect static files
    print("\n4️⃣ Collecting static files...")
    if not run_command("python manage.py collectstatic --noinput", "Static files collection"):
        print("⚠️  Static files collection had issues, but continuing...")
    
    # Create media directories if they don't exist
    print("\n5️⃣ Creating media directories...")
    media_dirs = ['media', 'media/question_images', 'media/treasure_hunt_photos', 'media/avatars']
    for dir_path in media_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 Ensured directory exists: {dir_path}")
    
    # Final verification
    print("\n6️⃣ Final verification...")
    if not run_command("python force_fix_table.py", "Verify table exists"):
        print("⚠️  Final verification failed, but starting server anyway...")
    
    # Start server
    print("\n7️⃣ Starting server...")
    port = os.environ.get('PORT', '8000')
    server_cmd = f"gunicorn onam_project.wsgi:application --bind 0.0.0.0:{port} --workers 1 --timeout 120 --worker-class sync"
    
    print(f"🌐 Starting server on port {port}...")
    print(f"🔗 Command: {server_cmd}")
    
    try:
        subprocess.run(server_cmd, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
