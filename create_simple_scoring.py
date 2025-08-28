#!/usr/bin/env python3
"""
Create Simple Event Scoring System
"""
import os
import sys

# Add current directory to Python path  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def create_simple_scoring_models():
    """Create simple scoring models"""
    
    model_code = '''
# Simple Event Scoring Model
class EventScoring(models.Model):
    """Simple event scoring system"""
    SCORING_TYPES = [
        ('team', 'Team Score (Group Event)'),
        ('individual', 'Individual Score'),
        ('team_individual', 'Team Score with Individual Participants'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='scores')
    team = models.CharField(max_length=20, help_text="Team code (e.g., team_1, team_2)")
    scoring_type = models.CharField(max_length=20, choices=SCORING_TYPES, default='team')
    points = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Points awarded")
    
    # For individual participants in team events
    participants = models.ManyToManyField(Player, blank=True, 
                                        help_text="Select individual participants (optional)")
    
    notes = models.TextField(blank=True, help_text="Optional notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['event', 'team']
        ordering = ['-points', 'team']
        verbose_name = "Event Score"
        verbose_name_plural = "Event Scores"
    
    def __str__(self):
        return f"{self.event.name} - {self.get_team_display()} - {self.points} pts"
    
    def get_team_display(self):
        """Get team display name"""
        try:
            from .models import TeamConfiguration
            return TeamConfiguration.get_team_name(self.team)
        except:
            return dict(Player.TEAM_CHOICES).get(self.team, self.team)
    
    @property
    def participant_count(self):
        """Get number of participants"""
        return self.participants.count()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update individual player scores if this is a team event with participants
        if self.scoring_type == 'team_individual' and self.participants.exists():
            self.update_participant_team_points()
    
    def update_participant_team_points(self):
        """Update team points for individual participants"""
        if self.points <= 0 or not self.participants.exists():
            return
        
        points_per_participant = self.points / self.participants.count()
        for participant in self.participants.all():
            # Add points to participant's individual score
            participant.score += int(points_per_participant)
            participant.save(update_fields=['score'])
'''
    
    return model_code

def create_scoring_view():
    """Create simple scoring view"""
    
    view_code = '''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from .models import Event, Player, EventScoring, TeamConfiguration

@staff_member_required
def simple_event_scoring(request):
    """Simple event scoring interface"""
    
    if request.method == 'POST':
        event_id = request.POST.get('event')
        team_code = request.POST.get('team')
        points = request.POST.get('points', 0)
        scoring_type = request.POST.get('scoring_type', 'team')
        participants = request.POST.getlist('participants')
        notes = request.POST.get('notes', '')
        
        try:
            event = get_object_or_404(Event, id=event_id, is_active=True)
            points = float(points) if points else 0
            
            # Create or update score
            score, created = EventScoring.objects.get_or_create(
                event=event,
                team=team_code,
                defaults={
                    'scoring_type': scoring_type,
                    'points': points,
                    'notes': notes
                }
            )
            
            if not created:
                score.scoring_type = scoring_type
                score.points = points
                score.notes = notes
                score.save()
            
            # Add participants if selected
            if scoring_type == 'team_individual' and participants:
                participant_players = Player.objects.filter(id__in=participants, team=team_code)
                score.participants.set(participant_players)
            else:
                score.participants.clear()
            
            action = "Created" if created else "Updated"
            team_name = TeamConfiguration.get_team_name(team_code)
            messages.success(request, f'{action} score: {event.name} - {team_name} - {points} points')
            
        except Exception as e:
            messages.error(request, f'Error saving score: {str(e)}')
        
        return redirect('core:simple_event_scoring')
    
    # GET request - show the form
    events = Event.objects.filter(is_active=True).order_by('name')
    teams = TeamConfiguration.objects.filter(is_active=True).order_by('team_code')
    players = Player.objects.filter(is_active=True).order_by('team', 'name')
    existing_scores = EventScoring.objects.select_related('event').prefetch_related('participants').order_by('-created_at')[:20]
    
    # Group players by team for easier selection
    teams_with_players = {}
    for team in teams:
        team_players = players.filter(team=team.team_code)
        teams_with_players[team] = team_players
    
    context = {
        'events': events,
        'teams': teams,
        'teams_with_players': teams_with_players,
        'existing_scores': existing_scores,
        'page_title': 'Simple Event Scoring'
    }
    
    return render(request, 'core/simple_event_scoring.html', context)

@staff_member_required
def delete_event_score(request, score_id):
    """Delete an event score"""
    if request.method == 'POST':
        try:
            score = get_object_or_404(EventScoring, id=score_id)
            event_name = score.event.name
            team_name = score.get_team_display()
            score.delete()
            messages.success(request, f'Deleted score: {event_name} - {team_name}')
        except Exception as e:
            messages.error(request, f'Error deleting score: {str(e)}')
    
    return redirect('core:simple_event_scoring')
'''
    
    return view_code

def create_scoring_template():
    """Create simple scoring template"""
    
    template_code = '''<!DOCTYPE html>
<html>
<head>
    <title>Simple Event Scoring - Onam Celebration</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #d4af37 0%, #ffd700 50%, #d4af37 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { 
            color: #d4af37; 
            text-align: center; 
            margin-bottom: 30px; 
            font-size: 2.5em;
        }
        .section { 
            margin: 30px 0; 
            padding: 25px; 
            background: #f8f9fa; 
            border-radius: 10px; 
            border-left: 5px solid #d4af37;
        }
        .form-group { 
            margin: 20px 0; 
        }
        label { 
            display: block; 
            font-weight: bold; 
            margin-bottom: 8px; 
            color: #333;
        }
        select, input[type="number"], input[type="text"], textarea { 
            width: 100%; 
            padding: 12px; 
            border: 2px solid #ddd; 
            border-radius: 8px; 
            font-size: 16px;
            box-sizing: border-box;
        }
        select:focus, input:focus, textarea:focus { 
            border-color: #d4af37; 
            outline: none; 
        }
        .btn { 
            background: #d4af37; 
            color: white; 
            padding: 12px 25px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 16px; 
            margin: 10px 5px 10px 0;
            font-weight: bold;
        }
        .btn:hover { 
            background: #b8941f; 
        }
        .btn-danger {
            background: #dc3545;
        }
        .btn-danger:hover {
            background: #c82333;
        }
        .success { 
            background: #d4edda; 
            color: #155724; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 15px 0; 
            border: 1px solid #c3e6cb;
        }
        .error { 
            background: #f8d7da; 
            color: #721c24; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 15px 0; 
            border: 1px solid #f5c6cb;
        }
        .score-table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 20px; 
        }
        .score-table th, .score-table td { 
            padding: 12px; 
            text-align: left; 
            border-bottom: 1px solid #ddd; 
        }
        .score-table th { 
            background: #d4af37; 
            color: white; 
        }
        .participants-select {
            display: none;
            margin-top: 15px;
        }
        .participants-select.show {
            display: block;
        }
        .team-players {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            background: #f9f9f9;
        }
        .team-players h4 {
            margin: 0 0 10px 0;
            color: #d4af37;
        }
        .checkbox-list {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            background: white;
        }
        .checkbox-item {
            margin: 5px 0;
        }
        .checkbox-item input {
            width: auto;
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 Simple Event Scoring</h1>
        
        {% if messages %}
            {% for message in messages %}
                <div class="{% if message.tags == 'error' %}error{% else %}success{% endif %}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        <!-- Scoring Form -->
        <div class="section">
            <h2>📋 Add/Update Event Score</h2>
            <form method="post" id="scoringForm">
                {% csrf_token %}
                
                <div class="form-group">
                    <label for="event">Select Event:</label>
                    <select name="event" id="event" required>
                        <option value="">Choose an event...</option>
                        {% for event in events %}
                        <option value="{{ event.id }}" data-participation="{{ event.participation_type }}">
                            {{ event.name }} ({{ event.get_participation_type_display }})
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="team">Select Team:</label>
                    <select name="team" id="team" required onchange="updateParticipants()">
                        <option value="">Choose a team...</option>
                        {% for team in teams %}
                        <option value="{{ team.team_code }}">{{ team.team_name }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="scoring_type">Scoring Type:</label>
                    <select name="scoring_type" id="scoring_type" onchange="toggleParticipants()">
                        <option value="team">Team Score (Group Event)</option>
                        <option value="individual">Individual Score</option>
                        <option value="team_individual">Team Score with Individual Participants</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="points">Points to Award:</label>
                    <input type="number" name="points" id="points" step="0.01" min="0" required placeholder="Enter points (e.g., 85.5)">
                </div>
                
                <div class="form-group participants-select" id="participantsSection">
                    <label>Select Individual Participants:</label>
                    <div id="participantsList">
                        <!-- Participants will be populated by JavaScript -->
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="notes">Notes (Optional):</label>
                    <textarea name="notes" id="notes" rows="3" placeholder="Any additional notes about the scoring..."></textarea>
                </div>
                
                <button type="submit" class="btn">💾 Save Score</button>
                <a href="/leaderboard/" class="btn" style="background: #6c757d; text-decoration: none;">📊 View Leaderboard</a>
            </form>
        </div>
        
        <!-- Existing Scores -->
        <div class="section">
            <h2>📈 Recent Scores</h2>
            {% if existing_scores %}
            <table class="score-table">
                <thead>
                    <tr>
                        <th>Event</th>
                        <th>Team</th>
                        <th>Points</th>
                        <th>Type</th>
                        <th>Participants</th>
                        <th>Date</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for score in existing_scores %}
                    <tr>
                        <td>{{ score.event.name }}</td>
                        <td>{{ score.get_team_display }}</td>
                        <td><strong>{{ score.points }}</strong></td>
                        <td>{{ score.get_scoring_type_display }}</td>
                        <td>
                            {% if score.participants.exists %}
                                {{ score.participant_count }} player{{ score.participant_count|pluralize }}
                            {% else %}
                                -
                            {% endif %}
                        </td>
                        <td>{{ score.created_at|date:"M d, H:i" }}</td>
                        <td>
                            <form method="post" action="{% url 'core:delete_event_score' score.id %}" style="display: inline;" 
                                  onsubmit="return confirm('Delete this score?')">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-danger" style="padding: 5px 10px; font-size: 12px;">🗑️ Delete</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p>No scores recorded yet. Add your first score above!</p>
            {% endif %}
        </div>
        
        <!-- Instructions -->
        <div class="section">
            <h2>📝 How to Use</h2>
            <ul>
                <li><strong>Team Score (Group Event):</strong> Award points to a team for group activities like group dance, drama</li>
                <li><strong>Individual Score:</strong> Award points to individuals that count toward their personal score</li>
                <li><strong>Team Score with Individual Participants:</strong> Award team points but also specify which individuals participated</li>
            </ul>
            <p><strong>💡 Tip:</strong> For group events with individual participants, the total points will be distributed among participants and added to their individual scores too!</p>
        </div>
    </div>
    
    <script>
        // Team players data
        const teamsWithPlayers = {
            {% for team, players in teams_with_players.items %}
            '{{ team.team_code }}': [
                {% for player in players %}
                {id: {{ player.id }}, name: '{{ player.name }}'},
                {% endfor %}
            ],
            {% endfor %}
        };
        
        function toggleParticipants() {
            const scoringType = document.getElementById('scoring_type').value;
            const participantsSection = document.getElementById('participantsSection');
            
            if (scoringType === 'team_individual') {
                participantsSection.classList.add('show');
                updateParticipants();
            } else {
                participantsSection.classList.remove('show');
            }
        }
        
        function updateParticipants() {
            const teamCode = document.getElementById('team').value;
            const participantsList = document.getElementById('participantsList');
            
            if (!teamCode || !teamsWithPlayers[teamCode]) {
                participantsList.innerHTML = '<p>Select a team first</p>';
                return;
            }
            
            const players = teamsWithPlayers[teamCode];
            if (players.length === 0) {
                participantsList.innerHTML = '<p>No players found for this team</p>';
                return;
            }
            
            let html = '<div class="checkbox-list">';
            players.forEach(player => {
                html += `
                    <div class="checkbox-item">
                        <input type="checkbox" name="participants" value="${player.id}" id="player_${player.id}">
                        <label for="player_${player.id}" style="display: inline; font-weight: normal;">${player.name}</label>
                    </div>
                `;
            });
            html += '</div>';
            
            participantsList.innerHTML = html;
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            toggleParticipants();
        });
    </script>
</body>
</html>'''
    
    return template_code

def main():
    print("🏆 CREATING SIMPLE EVENT SCORING SYSTEM")
    print("=" * 50)
    
    # Create model code
    model_code = create_simple_scoring_models()
    print("✅ Created EventScoring model code")
    
    # Create view code
    view_code = create_scoring_view()
    print("✅ Created simple_event_scoring view code")
    
    # Create template
    template_code = create_scoring_template()
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'core', 'simple_event_scoring.html')
    os.makedirs(os.path.dirname(template_path), exist_ok=True)
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_code)
    print(f"✅ Created template: {template_path}")
    
    # Save model code to file
    models_addition_path = os.path.join(os.path.dirname(__file__), 'simple_scoring_models.py')
    with open(models_addition_path, 'w', encoding='utf-8') as f:
        f.write(f"# Add this to your apps/core/models.py\\n\\n{model_code}")
    print(f"✅ Created model addition: {models_addition_path}")
    
    # Save view code to file
    views_addition_path = os.path.join(os.path.dirname(__file__), 'simple_scoring_views.py')
    with open(views_addition_path, 'w', encoding='utf-8') as f:
        f.write(f"# Add this to your apps/core/views.py\\n\\n{view_code}")
    print(f"✅ Created view addition: {views_addition_path}")
    
    print("\\n🎯 SETUP INSTRUCTIONS:")
    print("=" * 30)
    print("1. Add the EventScoring model to apps/core/models.py")
    print("2. Add the views to apps/core/views.py") 
    print("3. Add URL patterns to apps/core/urls.py:")
    print("   path('event-scoring/', views.simple_event_scoring, name='simple_event_scoring'),")
    print("   path('event-scoring/delete/<int:score_id>/', views.delete_event_score, name='delete_event_score'),")
    print("4. Run: python manage.py makemigrations")
    print("5. Run: python manage.py migrate")
    print("\\n🌐 Access at: /event-scoring/")
    print("\\n✨ Features:")
    print("   • Simple form: Event + Team + Score")
    print("   • Support for team events, individual events, and team+individual")
    print("   • Optional participant selection for team events")
    print("   • Recent scores table with delete option")
    print("   • No need to specify who awarded the score")
    print("   • Clean, responsive interface")

if __name__ == "__main__":
    main()
