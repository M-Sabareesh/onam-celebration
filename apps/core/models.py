from django.db import models
from django.contrib.auth.models import User

# Simple name selection model for Onam celebration
class Player(models.Model):
    """Enhanced player model that allows manual name entry"""
    
    # Teams for admin assignment
    TEAM_CHOICES = [
        ('team_1', 'Team 1'),
        ('team_2', 'Team 2'),
        ('team_3', 'Team 3'),
        ('team_4', 'Team 4'),
        ('unassigned', 'Unassigned'),
    ]
    
    name = models.CharField(max_length=100)  # Allow manual name entry
    team = models.CharField(max_length=20, choices=TEAM_CHOICES, default='unassigned')
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)  # Track online status
    current_level = models.PositiveIntegerField(default=1)
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    has_completed_hunt = models.BooleanField(default=False)
    session_key = models.CharField(max_length=50, blank=True, null=True)  # Store session
    
    class Meta:
        ordering = ['-score', '-last_activity']
        
    def __str__(self):
        return self.name
    
    @property
    def teammates(self):
        """Get list of teammates (excluding self)"""
        if self.team != 'unassigned':
            teammates = Player.objects.filter(team=self.team, is_active=True).exclude(id=self.id)
            return teammates
        return Player.objects.none()
    
    @property
    def online_teammates(self):
        """Get list of online teammates"""
        return self.teammates.filter(is_online=True)
    
    def mark_online(self):
        """Mark player as online"""
        self.is_online = True
        self.save(update_fields=['is_online', 'last_activity'])
    
    def mark_offline(self):
        """Mark player as offline"""
        self.is_online = False
        self.save(update_fields=['is_online'])


class GameSession(models.Model):
    """Track game sessions"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sessions')
    level = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.player.name} - Level {self.level}"


class TreasureHuntQuestion(models.Model):
    """Treasure hunt questions"""
    QUESTION_TYPES = [
        ('text', 'Text Answer'),
        ('photo', 'Photo Upload'),
        ('multiple_choice', 'Multiple Choice'),
        ('image_text', 'Image Question (Text Answer)'),
    ]
    
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_image = models.ImageField(upload_to='question_images/', blank=True, null=True, 
                                     help_text="Upload an image for image-based questions")
    order = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    
    # For multiple choice questions
    option_a = models.CharField(max_length=200, blank=True)
    option_b = models.CharField(max_length=200, blank=True)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)
    correct_answer = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."


class PlayerAnswer(models.Model):
    """Player answers to treasure hunt questions"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    question = models.ForeignKey(TreasureHuntQuestion, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True)
    photo_answer = models.ImageField(upload_to='treasure_hunt_photos/', blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    points_awarded = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['player', 'question']
    
    def __str__(self):
        return f"{self.player.name} - Q{self.question.order}"


class Event(models.Model):
    """Events for team competitions"""
    EVENT_TYPES = [
        ('group_dance', 'Group Dance'),
        ('group_song', 'Group Song'),
    ]
    
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    voting_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_event_type_display()})"
    
    @property
    def participating_teams(self):
        """Get teams that are participating in this event"""
        return self.eventparticipation_set.values_list('team', flat=True)
    
    @property
    def average_scores(self):
        """Get average scores for each team in this event (voting + admin scores)"""
        from django.db.models import Avg
        scores = {}
        for team_code, team_name in Player.TEAM_CHOICES:
            if team_code == 'unassigned':
                continue
                
            # Check if team has admin-awarded score
            admin_score = 0
            vote_count = 0
            try:
                event_score = EventScore.objects.get(event=self, team=team_code)
                admin_score = float(event_score.points)
            except EventScore.DoesNotExist:
                pass
            
            # Calculate voting scores if voting is enabled
            voting_score = 0
            if self.voting_enabled and team_code in self.participating_teams:
                votes = EventVote.objects.filter(event=self, performing_team=team_code)
                if votes.exists():
                    avg_coordination = votes.aggregate(Avg('coordination_score'))['coordination_score__avg'] or 0
                    avg_selection = votes.aggregate(Avg('selection_score'))['selection_score__avg'] or 0
                    avg_overall = votes.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
                    avg_enjoyment = votes.aggregate(Avg('enjoyment_score'))['enjoyment_score__avg'] or 0
                    
                    voting_score = (avg_coordination + avg_selection + avg_overall + avg_enjoyment) / 4
                    vote_count = votes.count()
            
            # Use admin score if available, otherwise use voting score
            final_score = admin_score if admin_score > 0 else voting_score
            
            if final_score > 0 or team_code in self.participating_teams:
                scores[team_code] = {
                    'coordination': 0,
                    'selection': 0,
                    'overall': 0,
                    'enjoyment': 0,
                    'total': round(final_score, 2),
                    'vote_count': vote_count,
                    'admin_score': admin_score,
                    'voting_score': round(voting_score, 2)
                }
        return scores


class EventParticipation(models.Model):
    """Teams participating in events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'team']
    
    def __str__(self):
        return f"{self.get_team_display()} - {self.event.name}"


class EventVote(models.Model):
    """Votes from teams for other teams' performances"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    voting_team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    performing_team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    
    # Scoring criteria (1-10 scale)
    coordination_score = models.PositiveIntegerField(
        help_text="Group Coordination (1-10)"
    )
    selection_score = models.PositiveIntegerField(
        help_text="Song/Dance Selection (1-10)"
    )
    overall_score = models.PositiveIntegerField(
        help_text="Overall Performance (1-10)"
    )
    enjoyment_score = models.PositiveIntegerField(
        help_text="Enjoying the Event (1-10)"
    )
    
    comments = models.TextField(blank=True, help_text="Optional feedback")
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'voting_team', 'performing_team']
    
    def __str__(self):
        return f"{self.get_voting_team_display()} votes for {self.get_performing_team_display()} - {self.event.name}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.voting_team == self.performing_team:
            raise ValidationError("Teams cannot vote for themselves")
    
    @property
    def total_score(self):
        return self.coordination_score + self.selection_score + self.overall_score + self.enjoyment_score
    
    @property
    def average_score(self):
        return self.total_score / 4


class EventScore(models.Model):
    """Admin-awarded scores for events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True, help_text="Optional notes about the scoring")
    awarded_by = models.CharField(max_length=100, help_text="Admin who awarded the points")
    awarded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'team']
        ordering = ['-points', 'team']
    
    def __str__(self):
        return f"{self.get_team_display()} - {self.event.name}: {self.points} pts"
