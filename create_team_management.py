#!/usr/bin/env python3
"""
Create Simple Team Management Page
Works without static files - direct HTML interface
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

try:
    import django
    django.setup()
    
    print("🔧 CREATING SIMPLE TEAM MANAGEMENT")
    print("=" * 40)
    
    # Create teams if they don't exist
    from apps.core.models import TeamConfiguration
    
    teams = [
        ('team_1', 'Team 1'),
        ('team_2', 'Team 2'), 
        ('team_3', 'Team 3'),
        ('team_4', 'Team 4'),
        ('unassigned', 'Unassigned')
    ]
    
    print("📋 Setting up default teams...")
    for team_code, team_name in teams:
        team, created = TeamConfiguration.objects.get_or_create(
            team_code=team_code,
            defaults={'team_name': team_name}
        )
        if created:
            print(f"   ✅ Created: {team_name}")
        else:
            print(f"   ✅ Exists: {team_name}")
    
    # Create simple team management template
    template_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Team Name Management - Onam Celebration</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #d4af37; text-align: center; margin-bottom: 30px; }
        .team-form { margin: 20px 0; padding: 20px; background: #f9f9f9; border-radius: 8px; border-left: 4px solid #d4af37; }
        .team-form h3 { margin-top: 0; color: #333; }
        input[type="text"] { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; margin: 10px 0; }
        input[type="text"]:focus { border-color: #d4af37; outline: none; }
        .btn { background: #d4af37; color: white; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px 5px; }
        .btn:hover { background: #b8941f; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .info { background: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .player-count { font-size: 14px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 Team Name Management</h1>
        <div class="info">
            <strong>Instructions:</strong> Change team names from "Team 1", "Team 2" etc. to any custom names you want. 
            These names will appear throughout the site including leaderboards and charts.
        </div>
        
        {% if success %}
        <div class="success">✅ Team names updated successfully!</div>
        {% endif %}
        
        <form method="post">
            {% csrf_token %}
            {% for team in teams %}
            <div class="team-form">
                <h3>{{ team.team_code|title }}</h3>
                <label>Team Name:</label>
                <input type="text" name="team_{{ team.team_code }}" value="{{ team.team_name }}" 
                       placeholder="Enter custom team name...">
                <div class="player-count">{{ team.player_count }}</div>
            </div>
            {% endfor %}
            
            <div style="text-align: center; margin-top: 30px;">
                <button type="submit" class="btn">💾 Save Team Names</button>
                <a href="/leaderboard/" class="btn" style="background: #6c757d; text-decoration: none;">📊 View Leaderboard</a>
            </div>
        </form>
        
        <div class="info" style="margin-top: 30px;">
            <strong>Example Team Names:</strong><br>
            • Mythological: "Maveli Squad", "Vamana Warriors", "Parashurama Force"<br>
            • Colors: "Red Warriors", "Blue Titans", "Green Guardians", "Golden Eagles"<br>  
            • Festival: "Pookalam Masters", "Thiruvathira Stars", "Onam Champions"
        </div>
    </div>
</body>
</html>'''
    
    # Save template
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'core')
    os.makedirs(template_dir, exist_ok=True)
    
    template_path = os.path.join(template_dir, 'team_management.html')
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"✅ Template created: {template_path}")
    
    # Create view
    view_content = '''
# Add this to your apps/core/views.py

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import TeamConfiguration, Player

@staff_member_required
def team_management(request):
    """Simple team management interface"""
    if request.method == 'POST':
        # Update team names
        for key, value in request.POST.items():
            if key.startswith('team_') and key != 'csrfmiddlewaretoken':
                team_code = key.replace('team_', '')
                if value.strip():
                    try:
                        team = TeamConfiguration.objects.get(team_code=team_code)
                        team.team_name = value.strip()
                        team.save()
                    except TeamConfiguration.DoesNotExist:
                        TeamConfiguration.objects.create(
                            team_code=team_code,
                            team_name=value.strip()
                        )
        
        messages.success(request, 'Team names updated successfully!')
        return redirect('core:team_management')
    
    # Get teams with player counts
    teams = []
    for team in TeamConfiguration.objects.all().order_by('team_code'):
        player_count = Player.objects.filter(team=team.team_code, is_active=True).count()
        teams.append({
            'team_code': team.team_code,
            'team_name': team.team_name,
            'player_count': f"{player_count} active players"
        })
    
    return render(request, 'core/team_management.html', {
        'teams': teams,
        'success': 'success' in request.GET
    })
'''
    
    print("📋 View code created (add to views.py):")
    print(view_content)
    
    # Create URL
    url_content = '''
# Add this to your apps/core/urls.py

from . import views

urlpatterns = [
    # ... existing urls ...
    path('team-management/', views.team_management, name='team_management'),
]
'''
    
    print("📋 URL code created (add to urls.py):")
    print(url_content)
    
    print("\n✅ TEAM MANAGEMENT SETUP COMPLETE!")
    print("🌐 After adding the view and URL, access at: /team-management/")
    print("🏆 This works without any static files!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
