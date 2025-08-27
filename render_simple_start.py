#!/usr/bin/env python3
"""
Simple Render Start Script
Just runs migrations and starts the server - no complex setup
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
            return True
        else:
            print(f"⚠️  {description} had issues: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    """Simple startup process"""
    print("🚀 RENDER STARTUP - SIMPLE VERSION")
    print("=" * 40)
    
    # Basic migrations only
    run_command("python manage.py migrate --noinput", "Database migrations")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Static files collection")
    
    # Start server
    port = os.environ.get('PORT', '8000')
    server_cmd = f"gunicorn onam_project.wsgi:application --bind 0.0.0.0:{port} --workers 1 --timeout 60"
    
    print(f"🌐 Starting server on port {port}...")
    
    try:
        subprocess.run(server_cmd, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
