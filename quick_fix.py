#!/usr/bin/env python3
"""
Quick Database Check and Fix
"""
import os
import sys

# Get the current directory (the project root)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🔧 QUICK DATABASE FIX")
print("=" * 30)

try:
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
    
    # Import Django and setup
    import django
    django.setup()
    
    print("✅ Django setup successful")
    
    # Import management command
    from django.core.management import call_command
    
    # Run migrations
    print("🔄 Running migrations...")
    call_command('migrate', verbosity=1, interactive=False)
    print("✅ Migrations completed")
    
    # Check TeamConfiguration
    print("🔍 Checking TeamConfiguration...")
    from apps.core.models import TeamConfiguration
    
    count = TeamConfiguration.objects.count()
    print(f"✅ TeamConfiguration table has {count} records")
    
    if count == 0:
        print("📋 Creating default teams...")
        teams = [
            ('team_1', 'Team Maveli'),
            ('team_2', 'Team Onam'),
            ('team_3', 'Team Thiruvonam'),
            ('team_4', 'Team Pookalam')
        ]
        
        for team_code, team_name in teams:
            team, created = TeamConfiguration.objects.get_or_create(
                team_code=team_code,
                defaults={'team_name': team_name}
            )
            if created:
                print(f"   ✅ Created: {team_name}")
    
    # Check admin access
    print("🔍 Checking admin access...")
    from django.contrib.auth.models import User
    admin_count = User.objects.filter(is_superuser=True).count()
    print(f"✅ Found {admin_count} admin users")
    
    if admin_count == 0:
        print("👤 Creating admin user...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Admin user created (username: admin, password: admin123)")
    
    print("\n🎉 DATABASE IS READY!")
    print("🌐 Run: python manage.py runserver")
    print("🏆 Admin: http://localhost:8000/admin/")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're in the project directory and Django is installed")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
