#!/usr/bin/env python3
"""
Ultimate Production Deployment Script
Handles all database issues and starts the server safely
"""
import os
import sys
import subprocess

def log(message):
    """Print a formatted log message"""
    print(f"🔧 {message}")

def error(message):
    """Print a formatted error message"""
    print(f"❌ {message}")

def success(message):
    """Print a formatted success message"""
    print(f"✅ {message}")

def run_django_setup():
    """Setup Django environment"""
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
        
        # Import and setup Django
        import django
        django.setup()
        
        success("Django environment setup complete")
        return True
    except Exception as e:
        error(f"Django setup failed: {e}")
        # Try with development settings
        try:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'onam_project.settings.development'
            import django
            django.setup()
            success("Django setup complete (development mode)")
            return True
        except Exception as e2:
            error(f"Django setup failed completely: {e2}")
            return False

def run_migrations():
    """Run Django migrations"""
    try:
        from django.core.management import call_command
        log("Running database migrations...")
        call_command('migrate', verbosity=1, interactive=False)
        success("Migrations completed successfully")
        return True
    except Exception as e:
        error(f"Migration failed: {e}")
        return False

def setup_team_configurations():
    """Setup team configurations"""
    try:
        from apps.core.models import TeamConfiguration
        
        log("Setting up team configurations...")
        teams = [
            ('team_1', 'Team Maveli'),
            ('team_2', 'Team Onam'),
            ('team_3', 'Team Thiruvonam'),
            ('team_4', 'Team Pookalam'),
            ('unassigned', 'Unassigned')
        ]
        
        for team_code, team_name in teams:
            config, created = TeamConfiguration.objects.get_or_create(
                team_code=team_code,
                defaults={'team_name': team_name}
            )
            if created:
                success(f"Created team: {team_name}")
            else:
                log(f"Team exists: {team_name}")
        
        success("Team configurations ready")
        return True
    except Exception as e:
        error(f"Team setup failed: {e}")
        return False

def create_admin_user():
    """Create admin user if needed"""
    try:
        from django.contrib.auth.models import User
        
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            success(f"Admin user '{username}' created")
        else:
            log(f"Admin user '{username}' exists")
        
        return True
    except Exception as e:
        error(f"Admin user creation failed: {e}")
        return False

def verify_deployment():
    """Verify deployment is ready"""
    try:
        from apps.core.models import TeamConfiguration, Player, Event
        
        log("Verifying deployment...")
        
        # Check team configurations
        team_count = TeamConfiguration.objects.count()
        log(f"Team configurations: {team_count}")
        
        # Check if basic tables exist
        player_count = Player.objects.count()
        event_count = Event.objects.count()
        
        log(f"Players: {player_count}, Events: {event_count}")
        
        success("Deployment verification complete")
        return True
    except Exception as e:
        error(f"Verification failed: {e}")
        return False

def collect_static():
    """Collect static files"""
    try:
        from django.core.management import call_command
        log("Collecting static files...")
        call_command('collectstatic', verbosity=1, interactive=False)
        success("Static files collected")
        return True
    except Exception as e:
        log(f"Static collection failed (may be normal): {e}")
        return True  # Don't fail deployment for static files

def start_server():
    """Start the server"""
    try:
        log("Starting server...")
        
        # Get port from environment or use default
        port = os.environ.get('PORT', '8000')
        
        # Check if we're in production (Render/Heroku)
        if 'RENDER' in os.environ or 'HEROKU' in os.environ:
            # Use gunicorn for production
            cmd = [
                'gunicorn', 
                'onam_project.wsgi:application',
                '--bind', f'0.0.0.0:{port}',
                '--workers', '3',
                '--timeout', '120'
            ]
        else:
            # Use Django dev server for local
            cmd = ['python', 'manage.py', 'runserver', f'0.0.0.0:{port}']
        
        success(f"Starting server on port {port}")
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        log("Server stopped by user")
    except Exception as e:
        error(f"Server start failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 ULTIMATE PRODUCTION DEPLOYMENT")
    print("=" * 50)
    
    # Step 1: Setup Django
    if not run_django_setup():
        return False
    
    # Step 2: Run migrations
    if not run_migrations():
        return False
    
    # Step 3: Setup teams
    if not setup_team_configurations():
        return False
    
    # Step 4: Create admin
    if not create_admin_user():
        return False
    
    # Step 5: Collect static files
    collect_static()
    
    # Step 6: Verify deployment
    if not verify_deployment():
        return False
    
    success("🎉 DEPLOYMENT READY!")
    print("🌐 Your Onam Celebration site is now running!")
    print("🏆 Admin panel available at /admin/")
    
    # Step 7: Start server
    start_server()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Deployment stopped by user")
    except Exception as e:
        error(f"Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
