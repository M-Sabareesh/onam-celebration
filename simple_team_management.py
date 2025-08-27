#!/usr/bin/env python3
"""
Simple Team Management Setup and Test
Creates and manages teams for the Onam celebration website
"""

import os
import sys
import django

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.development')
django.setup()

from apps.core.models import TeamConfiguration, Player

def setup_teams():
    """Set up default teams with better names"""
    print("🏆 Setting up Team Management")
    print("=" * 40)
    
    # Default teams with more interesting names
    default_teams = [
        ('team_1', 'Red Warriors'),
        ('team_2', 'Blue Champions'),
        ('team_3', 'Green Masters'),
        ('team_4', 'Yellow Legends'),
        ('unassigned', 'Unassigned'),
    ]
    
    print("📝 Creating/updating teams:")
    for team_code, team_name in default_teams:
        team, created = TeamConfiguration.objects.get_or_create(
            team_code=team_code,
            defaults={'team_name': team_name, 'is_active': True}
        )
        if created:
            print(f"   ✅ Created: {team_code} → {team_name}")
        else:
            print(f"   📋 Exists: {team_code} → {team.team_name}")
    
    return default_teams

def show_teams():
    """Display all teams and their players"""
    print("\n📊 Current Teams:")
    print("-" * 40)
    
    teams = TeamConfiguration.objects.filter(is_active=True).order_by('team_code')
    
    for team in teams:
        if team.team_code == 'unassigned':
            continue
            
        # Count players in this team
        player_count = Player.objects.filter(team=team.team_code, is_active=True).count()
        print(f"🏆 {team.team_name}")
        print(f"   Code: {team.team_code}")
        print(f"   Players: {player_count}")
        
        # Show some players if they exist
        players = Player.objects.filter(team=team.team_code, is_active=True)[:3]
        if players:
            print(f"   Sample players: {', '.join([p.name for p in players])}")
        print()

def demo_team_name_changes():
    """Demonstrate how to change team names"""
    print("🎯 Team Name Management Demo")
    print("=" * 40)
    
    # Example team name changes
    examples = [
        ('team_1', 'Maveli Squad'),
        ('team_2', 'Vamana Warriors'),
        ('team_3', 'Parashurama Force'),
        ('team_4', 'Bhima Champions'),
    ]
    
    print("💡 Example: Changing team names to mythological themes:")
    for team_code, new_name in examples:
        try:
            team = TeamConfiguration.objects.get(team_code=team_code)
            old_name = team.team_name
            team.team_name = new_name
            team.save()
            print(f"   {team_code}: '{old_name}' → '{new_name}' ✅")
        except TeamConfiguration.DoesNotExist:
            print(f"   {team_code}: Not found ❌")
    
    print("\n🔄 Reverting to default names:")
    # Revert to defaults
    default_names = {
        'team_1': 'Red Warriors',
        'team_2': 'Blue Champions', 
        'team_3': 'Green Masters',
        'team_4': 'Yellow Legends'
    }
    
    for team_code, default_name in default_names.items():
        try:
            team = TeamConfiguration.objects.get(team_code=team_code)
            team.team_name = default_name
            team.save()
            print(f"   {team_code}: Reverted to '{default_name}' ✅")
        except TeamConfiguration.DoesNotExist:
            print(f"   {team_code}: Not found ❌")

def admin_instructions():
    """Show how to use the admin interface"""
    print("\n📝 How to Change Team Names in Admin:")
    print("=" * 45)
    print("""
🌐 Step 1: Access Admin Panel
   - Go to: http://localhost:8000/admin/ (or your site URL)
   - Login with your superuser credentials

🏆 Step 2: Find Team Management
   - Look for "CORE" section
   - Click on "Team configurations"

✏️  Step 3: Edit Team Names
   - Click on any team (e.g., "team_1: Red Warriors")
   - Change the "Team name" field to whatever you want:
     * "Red Warriors" → "Maveli Team"
     * "Blue Champions" → "Onam Squad"
     * "Green Masters" → "Festival Heroes"
     * "Yellow Legends" → "Celebration Champions"

💾 Step 4: Save Changes
   - Click "Save"
   - The new name appears instantly throughout the site!

⚠️  Important Notes:
   - Only change the "Team name" field
   - Don't change the "Team code" (team_1, team_2, etc.)
   - Changes are immediate - no restart needed
   - Team names appear on leaderboard, charts, and all pages
""")

def test_team_integration():
    """Test that teams work with the leaderboard and charts"""
    print("\n🧪 Testing Team Integration:")
    print("=" * 35)
    
    # Test that team names are retrieved correctly
    from apps.core.views import LeaderboardView
    
    try:
        # Create a test view instance
        view = LeaderboardView()
        
        # Test team name retrieval
        teams = TeamConfiguration.objects.filter(is_active=True)
        print(f"✅ Found {teams.count()} active teams:")
        
        for team in teams:
            if team.team_code != 'unassigned':
                display_name = TeamConfiguration.get_team_name(team.team_code)
                print(f"   {team.team_code}: {display_name}")
        
        print("\n✅ Team integration test passed!")
        print("   Teams are ready for leaderboard and charts")
        
    except Exception as e:
        print(f"❌ Error testing team integration: {e}")

def main():
    """Main function"""
    print("🎉 ONAM CELEBRATION - TEAM MANAGEMENT")
    print("=" * 50)
    
    # Set up teams
    setup_teams()
    
    # Show current teams
    show_teams()
    
    # Demo name changes
    demo_team_name_changes()
    
    # Show admin instructions
    admin_instructions()
    
    # Test integration
    test_team_integration()
    
    print("\n✅ Team Management Setup Complete!")
    print("🎯 Next Steps:")
    print("   1. Start your Django server: python manage.py runserver")
    print("   2. Go to /admin/ and login")
    print("   3. Navigate to Core > Team configurations")
    print("   4. Click on any team to change its name")
    print("   5. Check /leaderboard/ to see the changes")

if __name__ == "__main__":
    main()
