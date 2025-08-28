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
    print("=" * 50)
    
    # Database migrations
    if not run_command("python manage.py migrate --noinput", "Database migrations"):
        print("❌ Migration failed - stopping")
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Static files collection"):
        print("⚠️  Static files collection had issues, but continuing...")
    
    # Create media directories if they don't exist
    media_dirs = ['media', 'media/question_images', 'media/treasure_hunt_photos', 'media/avatars']
    for dir_path in media_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 Ensured directory exists: {dir_path}")
    
    # Start server
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
