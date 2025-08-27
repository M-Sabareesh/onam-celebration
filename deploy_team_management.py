#!/usr/bin/env python3
"""
Deploy Team Management System
Works independently of static files
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def main():
    print("🚀 DEPLOYING TEAM MANAGEMENT SYSTEM")
    print("=" * 45)
    
    try:
        import django
        django.setup()
        
        # Create default teams
        from apps.core.models import TeamConfiguration, Player
        from django.contrib.auth.models import User
        
        print("📋 Setting up team configurations...")
        teams = [
            ('team_1', 'Team 1'),
            ('team_2', 'Team 2'), 
            ('team_3', 'Team 3'),
            ('team_4', 'Team 4'),
            ('unassigned', 'Unassigned')
        ]
        
        for team_code, team_name in teams:
            team, created = TeamConfiguration.objects.get_or_create(
                team_code=team_code,
                defaults={'team_name': team_name}
            )
            if created:
                print(f"   ✅ Created: {team_name}")
            else:
                print(f"   ✅ Exists: {team_name}")
        
        # Create admin user if needed
        print("👤 Setting up admin user...")
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("   ✅ Admin user created (admin/admin123)")
        else:
            print("   ✅ Admin user exists")
        
        # Create some sample players for testing
        print("👥 Setting up sample players...")
        sample_players = [
            ('Alice', 'team_1'),
            ('Bob', 'team_2'),
            ('Charlie', 'team_3'),
            ('Diana', 'team_4'),
        ]
        
        for name, team in sample_players:
            player, created = Player.objects.get_or_create(
                name=name,
                defaults={'team': team, 'is_active': True}
            )
            if created:
                print(f"   ✅ Created player: {name} ({team})")
        
        print("\n🎉 TEAM MANAGEMENT SYSTEM READY!")
        print("=" * 45)
        print("📍 Access team management at: /team-management/")
        print("🏆 Features available:")
        print("   • Change team names from Team 1/2/3/4 to custom names")
        print("   • See player counts for each team") 
        print("   • Works without static files!")
        print("   • Updates reflect immediately on leaderboard and charts")
        print("\n🔐 Admin Access:")
        print("   • Username: admin")
        print("   • Password: admin123")
        print("   • Admin panel: /custom-admin/")
        print("\n🌐 Example URLs:")
        print("   • Team Management: https://your-site.com/team-management/")
        print("   • Leaderboard: https://your-site.com/leaderboard/")
        print("   • Homepage: https://your-site.com/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Setup complete! Your team management system is ready.")
    else:
        print("\n❌ Setup failed. Check the errors above.")
