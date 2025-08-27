#!/usr/bin/env python3
"""
Script to help update team names for Onam celebration
"""

import os
import sys

def show_current_teams():
    """Display current team configuration"""
    print("🔍 Current Team Configuration:")
    print("=" * 40)
    
    models_file = 'apps/core/models.py'
    if os.path.exists(models_file):
        with open(models_file, 'r') as f:
            lines = f.readlines()
            
        in_team_choices = False
        for line in lines:
            if 'TEAM_CHOICES = [' in line:
                in_team_choices = True
                print("📋 Current TEAM_CHOICES:")
            elif in_team_choices and line.strip().startswith(']'):
                in_team_choices = False
                break
            elif in_team_choices and line.strip():
                print(f"   {line.strip()}")
    else:
        print("❌ models.py not found")

def suggest_team_names():
    """Suggest different team naming themes"""
    print("\n🎯 Suggested Team Name Themes:")
    print("=" * 40)
    
    themes = {
        "Kerala Districts": [
            "('team_1', 'Thiruvananthapuram Tigers')",
            "('team_2', 'Kochi Champions')",
            "('team_3', 'Kozhikode Warriors')",
            "('team_4', 'Thrissur Legends')",
        ],
        "Onam Festival": [
            "('team_1', 'Maveli Warriors')",
            "('team_2', 'Pookalam Artists')",
            "('team_3', 'Pulikali Dancers')",
            "('team_4', 'Sadya Champions')",
        ],
        "Kerala Culture": [
            "('team_1', 'Kathakali Masters')",
            "('team_2', 'Mohiniyattam Artists')",
            "('team_3', 'Theyyam Performers')",
            "('team_4', 'Kalaripayattu Warriors')",
        ]
    }
    
    for theme, teams in themes.items():
        print(f"\n🏆 {theme} Theme:")
        for team in teams:
            print(f"   {team}")
        print("   ('unassigned', 'Unassigned'),")

def generate_migration_code():
    """Generate code for updating team names"""
    print("\n🔧 Implementation Steps:")
    print("=" * 40)
    
    print("\n1️⃣ Update apps/core/models.py:")
    print("   Replace the TEAM_CHOICES list with your preferred theme")
    
    print("\n2️⃣ Create migration:")
    print("   python manage.py makemigrations core")
    
    print("\n3️⃣ Apply migration:")
    print("   python manage.py migrate")
    
    print("\n4️⃣ Update chart colors (already done):")
    print("   ✅ Color mapping in views.py already updated")
    
    print("\n5️⃣ Test the changes:")
    print("   - Visit /admin/core/player/ to see new team names")
    print("   - Check /leaderboard/ for updated team names in chart")
    print("   - Verify colors are distinct for each team")

def main():
    print("👥 Team Name Management Tool")
    print("=" * 50)
    
    show_current_teams()
    suggest_team_names()
    generate_migration_code()
    
    print("\n✨ Summary:")
    print("   • Current teams are Team 1, Team 2, Team 3, Team 4")
    print("   • Chart colors are already fixed for correct team codes")
    print("   • Choose a theme and update TEAM_CHOICES in models.py")
    print("   • Run migrations to apply changes")
    print("   • Team names will update throughout the entire site")
    
    print("\n📚 For detailed instructions, see:")
    print("   📄 TEAM_NAME_MANAGEMENT_GUIDE.md")

if __name__ == '__main__':
    main()
