#!/usr/bin/env python3
"""
Safe Production Startup Script
Handles database setup before starting the server
"""

import os
import sys
import django
import subprocess

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def run_emergency_fix():
    """Run the emergency fix if needed"""
    print("🔧 Checking database state...")
    
    try:
        django.setup()
        from django.db import connection
        from apps.core.models import TeamConfiguration
        
        # Test if TeamConfiguration table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM core_teamconfiguration LIMIT 1;")
        
        print("✅ Database tables exist")
        return True
        
    except Exception as e:
        print(f"❌ Database issue detected: {e}")
        print("🛠️  Running emergency fix...")
        
        try:
            result = subprocess.run([sys.executable, 'emergency_production_fix.py'], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Emergency fix completed successfully")
                return True
            else:
                print(f"⚠️  Emergency fix had issues: {result.stderr}")
                return False
                
        except Exception as fix_error:
            print(f"❌ Emergency fix failed: {fix_error}")
            return False

def start_server():
    """Start the Gunicorn server"""
    print("🚀 Starting production server...")
    
    # Get port from environment (Render uses PORT)
    port = os.environ.get('PORT', '8000')
    
    # Start Gunicorn
    cmd = [
        'gunicorn',
        'onam_project.wsgi:application',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120',
        '--access-logfile', '-',
        '--error-logfile', '-',
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main startup function"""
    print("🎉 ONAM CELEBRATION - PRODUCTION STARTUP")
    print("=" * 50)
    
    # Run emergency fix if needed
    fix_success = run_emergency_fix()
    
    if not fix_success:
        print("⚠️  Database issues detected but continuing...")
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
