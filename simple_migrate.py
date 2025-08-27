#!/usr/bin/env python3
"""
Simple Migration Script - Run Django migrations
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')

# Setup Django
django.setup()

print("🔧 Running Django migrations...")

try:
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("✅ Migrations completed successfully!")
    
    # Check if TeamConfiguration table exists
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_teamconfiguration';")
        result = cursor.fetchone()
        if result:
            print("✅ TeamConfiguration table exists!")
        else:
            print("❌ TeamConfiguration table still missing!")
            
    # Create team configurations
    from apps.core.models import TeamConfiguration
    
    team_configs = [
        {'team_code': 'team_1', 'team_name': 'Team Maveli'},
        {'team_code': 'team_2', 'team_name': 'Team Onam'},
        {'team_code': 'team_3', 'team_name': 'Team Thiruvonam'},
        {'team_code': 'team_4', 'team_name': 'Team Pookalam'}
    ]
    
    for config in team_configs:
        team_config, created = TeamConfiguration.objects.get_or_create(
            team_code=config['team_code'],
            defaults={'team_name': config['team_name']}
        )
        if created:
            print(f"✅ Created team configuration: {config['team_name']}")
        else:
            print(f"✅ Team configuration already exists: {config['team_name']}")
    
    print("🎉 Setup complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
