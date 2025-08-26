#!/usr/bin/env python
"""
Complete Fix Script for Onam Celebration Project
This script fixes database migrations and static file issues.

Run this script to resolve:
1. Missing participation_type column error
2. Static files manifest issues with Maveli images
3. Team event participation system setup
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        return False

def fix_database_migrations():
    """Fix database migration issues"""
    print("=== Fixing Database Migrations ===\n")
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Check if virtual environment exists
    venv_python = project_dir / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        python_cmd = str(venv_python)
        print(f"✅ Using virtual environment: {python_cmd}")
    else:
        python_cmd = "python"
        print("⚠️  Using system Python")
    
    # Run migrations in order
    commands = [
        (f'{python_cmd} manage.py makemigrations', "Generate any missing migrations"),
        (f'{python_cmd} manage.py migrate core 0009', "Apply migration 0009 (EventScore)"),
        (f'{python_cmd} manage.py migrate core 0010', "Apply migration 0010 (Individual Events + participation_type)"),
        (f'{python_cmd} manage.py migrate core 0011', "Apply migration 0011 (Fix Individual Vote fields)"),
        (f'{python_cmd} manage.py migrate core 0012', "Apply migration 0012 (Team Event Participation)"),
        (f'{python_cmd} manage.py migrate', "Apply all remaining migrations"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        print()  # Add spacing
    
    return success_count == len(commands)

def fix_static_files():
    """Fix static file issues"""
    print("=== Fixing Static Files ===\n")
    
    project_dir = Path(__file__).parent
    
    # Ensure static directories exist
    static_dir = project_dir / "static" / "images"
    static_dir.mkdir(parents=True, exist_ok=True)
    
    media_dir = project_dir / "media" / "Maveli"
    
    # Copy Maveli images from media to static if they exist
    maveli_images = ["Maveli.jpg", "Maveli2.jpg", "Maveli2.png", "Maveli4.jpg"]
    
    for img in maveli_images:
        media_img = media_dir / img
        static_img = static_dir / img
        
        if media_img.exists():
            try:
                import shutil
                shutil.copy2(media_img, static_img)
                print(f"✅ Copied {img} to static/images/")
            except Exception as e:
                print(f"❌ Failed to copy {img}: {e}")
        elif not static_img.exists():
            # Create a minimal placeholder
            static_img.touch()
            print(f"📝 Created placeholder {img}")
    
    # Collect static files
    venv_python = project_dir / ".venv" / "Scripts" / "python.exe"
    python_cmd = str(venv_python) if venv_python.exists() else "python"
    
    return run_command(f'{python_cmd} manage.py collectstatic --noinput', "Collect static files")

def create_team_event_demo():
    """Create demo data for team event participation"""
    print("\n=== Creating Team Event Demo Data ===\n")
    
    demo_script = """
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
django.setup()

from apps.core.models import Event, EventScore, Player, TeamEventParticipation

# Create a sample team event
event, created = Event.objects.get_or_create(
    name="Group Dance Competition",
    defaults={
        'event_type': 'performance',
        'participation_type': 'team',
        'description': 'Team dance performance with participant tracking',
        'voting_enabled': True
    }
)

if created:
    print(f"✅ Created event: {event.name}")
else:
    print(f"✅ Event already exists: {event.name}")

# Create sample team score with auto-calculation
team_score, created = EventScore.objects.get_or_create(
    event=event,
    team='red_team',
    defaults={
        'points_per_participant': 10,
        'auto_calculate_points': True,
        'notes': 'Demo: 10 points per participant',
        'awarded_by': 'Admin'
    }
)

if created:
    print(f"✅ Created team score for Red Team")
    
    # Add some sample participants
    red_players = Player.objects.filter(team='red_team', is_active=True)[:5]
    for i, player in enumerate(red_players):
        participation, created = TeamEventParticipation.objects.get_or_create(
            event_score=team_score,
            player=player,
            defaults={'participated': i < 3}  # First 3 participate
        )
        if created:
            status = "participating" if participation.participated else "not participating"
            print(f"  - {player.name}: {status}")
    
    # Recalculate points
    team_score.save()
    print(f"✅ Total points calculated: {team_score.points} ({team_score.participant_count} participants × {team_score.points_per_participant})")

print("\\n🎉 Demo data created successfully!")
print("\\nTo test:")
print("1. Go to Django admin > Event Scores")
print("2. Edit the 'Group Dance Competition' score for Red Team")
print("3. Use checkboxes to select/deselect participants")
print("4. See points auto-calculate based on participants")
"""
    
    # Write demo script
    with open("create_demo_team_event.py", "w") as f:
        f.write(demo_script)
    
    print("📝 Created create_demo_team_event.py")
    
    # Run the demo script
    venv_python = Path(__file__).parent / ".venv" / "Scripts" / "python.exe"
    python_cmd = str(venv_python) if venv_python.exists() else "python"
    
    return run_command(f'{python_cmd} create_demo_team_event.py', "Create demo team event data")

def main():
    """Main function"""
    print("🔧 Onam Celebration Project - Complete Fix Script")
    print("=" * 60)
    
    success = True
    
    # Fix database migrations
    if not fix_database_migrations():
        print("❌ Database migration fixes failed")
        success = False
    
    # Fix static files
    if not fix_static_files():
        print("❌ Static file fixes failed")
        success = False
    
    # Create demo data
    if not create_team_event_demo():
        print("⚠️  Demo data creation failed (not critical)")
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All fixes completed successfully!")
        print("\n✅ Your team event participation system is now ready!")
        print("\nFeatures available:")
        print("• Checkbox selection of team members who participated")
        print("• Auto-calculation of points based on participant count")
        print("• Enhanced admin interface with live score preview")
        print("• Malayalam branding with Maveli images")
        print("\nNext steps:")
        print("1. Start your Django server: python manage.py runserver")
        print("2. Go to admin > Event Scores")
        print("3. Create/edit team event scores")
        print("4. Use checkboxes to select participants")
        print("5. Watch points auto-calculate!")
    else:
        print("❌ Some fixes failed. Check the output above for details.")
        print("\nManual steps to try:")
        print("1. python manage.py migrate")
        print("2. python manage.py collectstatic")
        print("3. Check logs for specific errors")

if __name__ == '__main__':
    main()
