#!/usr/bin/env python3
"""
FINAL EMERGENCY DEPLOYMENT SCRIPT
Fixes database + static files + starts server
"""
import os
import sys
import subprocess

def log(message):
    print(f"🔧 {message}")

def success(message):
    print(f"✅ {message}")

def error(message):
    print(f"❌ {message}")

def setup_django():
    """Setup Django environment"""
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
        
        import django
        django.setup()
        
        success("Django setup complete")
        return True
    except Exception as e:
        error(f"Django setup failed: {e}")
        return False

def run_migrations():
    """Run migrations"""
    try:
        log("Running migrations...")
        from django.core.management import call_command
        call_command('migrate', verbosity=0, interactive=False)
        success("Migrations complete")
        return True
    except Exception as e:
        error(f"Migrations failed: {e}")
        return False

def setup_teams():
    """Setup team configurations"""
    try:
        log("Setting up teams...")
        from apps.core.models import TeamConfiguration
        
        teams = [
            ('team_1', 'Team Maveli'),
            ('team_2', 'Team Onam'),
            ('team_3', 'Team Thiruvonam'),
            ('team_4', 'Team Pookalam'),
        ]
        
        for code, name in teams:
            team, created = TeamConfiguration.objects.get_or_create(
                team_code=code,
                defaults={'team_name': name}
            )
            if created:
                log(f"Created: {name}")
        
        success("Teams setup complete")
        return True
    except Exception as e:
        error(f"Teams setup failed: {e}")
        return False

def collect_static():
    """Collect static files"""
    try:
        log("Collecting static files...")
        from django.core.management import call_command
        call_command('collectstatic', verbosity=0, interactive=False, clear=True)
        success("Static files collected")
        return True
    except Exception as e:
        log(f"Static collection warning: {e}")
        return True  # Don't fail for static files

def create_admin():
    """Create admin user"""
    try:
        log("Creating admin user...")
        from django.contrib.auth.models import User
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            success("Admin user created (admin/admin123)")
        else:
            success("Admin user exists")
        
        return True
    except Exception as e:
        error(f"Admin creation failed: {e}")
        return False

def start_server():
    """Start the server"""
    try:
        log("Starting server...")
        
        port = os.environ.get('PORT', '8000')
        
        cmd = [
            'gunicorn',
            'onam_project.wsgi:application',
            '--bind', f'0.0.0.0:{port}',
            '--workers', '2',
            '--timeout', '120'
        ]
        
        success(f"Server starting on port {port}")
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        log("Server stopped")
    except Exception as e:
        error(f"Server error: {e}")

def main():
    """Main function"""
    print("🚀 FINAL EMERGENCY DEPLOYMENT")
    print("=" * 40)
    
    if not setup_django():
        return False
    
    if not run_migrations():
        return False
    
    if not setup_teams():
        return False
    
    collect_static()
    
    if not create_admin():
        return False
    
    success("🎉 DEPLOYMENT READY!")
    start_server()
    
    return True

if __name__ == "__main__":
    main()
