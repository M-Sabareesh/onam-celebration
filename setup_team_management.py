#!/usr/bin/env python3
"""
Setup script for Admin Team Management
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
django.setup()

def run_migrations():
    """Run migrations for team management"""
    import subprocess
    
    print("🔄 Running migrations for team management...")
    
    try:
        # Create migrations
        result = subprocess.run(['python', 'manage.py', 'makemigrations', 'core'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migration files created successfully")
        else:
            print(f"⚠️  Migration creation output: {result.stdout}")
            print(f"⚠️  Migration creation errors: {result.stderr}")
        
        # Apply migrations
        result = subprocess.run(['python', 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations applied successfully")
            return True
        else:
            print(f"❌ Migration failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

def create_initial_teams():
    """Create initial team configurations"""
    try:
        from apps.core.models import TeamConfiguration
        
        print("🏆 Creating initial team configurations...")
        
        default_teams = [
            ('team_1', 'Team 1'),
            ('team_2', 'Team 2'),
            ('team_3', 'Team 3'),
            ('team_4', 'Team 4'),
            ('unassigned', 'Unassigned'),
        ]
        
        created_count = 0
        for team_code, team_name in default_teams:
            team, created = TeamConfiguration.objects.get_or_create(
                team_code=team_code,
                defaults={'team_name': team_name, 'is_active': True}
            )
            if created:
                created_count += 1
                print(f"   ✅ Created team: {team_code} → {team_name}")
            else:
                print(f"   ℹ️  Team exists: {team_code} → {team.team_name}")
        
        print(f"✅ Team setup complete! Created {created_count} new teams")
        return True
        
    except Exception as e:
        print(f"❌ Error creating teams: {e}")
        return False

def test_team_display():
    """Test that team display works correctly"""
    try:
        from apps.core.models import Player, TeamConfiguration
        
        print("🧪 Testing team display functionality...")
        
        # Test TeamConfiguration.get_team_name
        for team_code in ['team_1', 'team_2', 'team_3', 'team_4']:
            team_name = TeamConfiguration.get_team_name(team_code)
            print(f"   📋 {team_code} → {team_name}")
        
        # Test Player.get_team_display if players exist
        sample_player = Player.objects.first()
        if sample_player:
            display_name = sample_player.get_team_display()
            print(f"   👤 Sample player team: {sample_player.team} → {display_name}")
        
        print("✅ Team display functionality working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error testing team display: {e}")
        return False

def main():
    print("🏆 Admin Team Management Setup")
    print("=" * 50)
    
    # Step 1: Run migrations
    if not run_migrations():
        print("❌ Migration failed, aborting setup")
        return
    
    # Step 2: Create initial teams
    if not create_initial_teams():
        print("❌ Team creation failed")
        return
    
    # Step 3: Test functionality
    if not test_team_display():
        print("❌ Team display test failed")
        return
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("✅ Team management is now ready!")
    print("")
    print("📋 Next Steps:")
    print("1. Go to your admin panel: /admin/")
    print("2. Look for 'Team configurations' section")
    print("3. Click on any team to edit its name")
    print("4. Changes will appear immediately throughout the site")
    print("")
    print("🎯 Suggested team names:")
    print("   • Thiruvananthapuram Tigers")
    print("   • Kochi Champions")
    print("   • Kozhikode Warriors")
    print("   • Thrissur Legends")
    print("")
    print("📚 For detailed instructions, see:")
    print("   📄 ADMIN_TEAM_MANAGEMENT_GUIDE.md")

if __name__ == '__main__':
    main()
