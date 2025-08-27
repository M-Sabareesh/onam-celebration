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
    """Events for team and individual competitions"""
    EVENT_TYPES = [
        ('group_dance', 'Group Dance'),
        ('group_song', 'Group Song'),
        ('individual_dance', 'Individual Dance'),
        ('individual_song', 'Individual Song'),
        ('individual_art', 'Individual Art'),
        ('individual_quiz', 'Individual Quiz'),
        ('individual_speech', 'Individual Speech'),
    ]
    
    PARTICIPATION_TYPES = [
        ('team', 'Team Event'),
        ('individual', 'Individual Event'),
        ('both', 'Both Team and Individual'),
    ]
    
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    participation_type = models.CharField(max_length=20, choices=PARTICIPATION_TYPES, default='team')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    voting_enabled = models.BooleanField(default=False)
    individual_points_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.0, 
                                                      help_text="Multiplier for individual points that go to team")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_event_type_display()})"
    
    @property
    def allows_individual_participation(self):
        """Check if event allows individual participation"""
        return self.participation_type in ['individual', 'both']
    
    @property
    def allows_team_participation(self):
        """Check if event allows team participation"""
        return self.participation_type in ['team', 'both']
    
    @property
    def participating_teams(self):
        """Get teams that are participating in this event"""
        return self.eventparticipation_set.values_list('team', flat=True)
    
    @property
    def participating_players(self):
        """Get players that are participating in this event individually"""
        return self.individualparticipation_set.values_list('player', flat=True)
    
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


class IndividualParticipation(models.Model):
    """Individual players participating in events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'player']
    
    def __str__(self):
        return f"{self.player.name} - {self.event.name}"


class IndividualEventScore(models.Model):
    """Scores for individual players in events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    team_points = models.DecimalField(max_digits=5, decimal_places=2, default=0, 
                                     help_text="Points contributed to player's team")
    notes = models.TextField(blank=True, help_text="Optional notes about the scoring")
    awarded_by = models.CharField(max_length=100, help_text="Admin who awarded the points")
    awarded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'player']
        ordering = ['-points', 'player__name']
    
    def save(self, *args, **kwargs):
        """Automatically calculate team points based on multiplier"""
        if self.event and self.points:
            self.team_points = float(self.points) * float(self.event.individual_points_multiplier)
        super().save(*args, **kwargs)
        
        # Update player's total score
        if self.player:
            self.update_player_score()
    
    def update_player_score(self):
        """Update the player's total score from treasure hunt, individual events, and team events"""
        from django.db.models import Sum
        
        # Get treasure hunt score
        treasure_hunt_score = PlayerAnswer.objects.filter(
            player=self.player, 
            is_correct=True
        ).aggregate(Sum('points_awarded'))['points_awarded__sum'] or 0
        
        # Get individual event scores
        individual_event_score = IndividualEventScore.objects.filter(
            player=self.player
        ).aggregate(Sum('points'))['points__sum'] or 0
        
        # Get team event contributions (this player's share of team events they participated in)
        team_event_total = 0
        for event_score in EventScore.objects.filter(team=self.player.team):
            participants = event_score.get_participants()
            if participants.filter(player=self.player).exists() and participants.count() > 0:
                team_event_total += float(event_score.points) / participants.count()
        
        # Update player's total score
        new_total = treasure_hunt_score + float(individual_event_score) + team_event_total
        self.player.score = new_total
        self.player.save(update_fields=['score'])
    
    def __str__(self):
        return f"{self.player.name} - {self.event.name}: {self.points} pts"


class IndividualEventVote(models.Model):
    """Votes for individual player performances"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    voting_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='votes_given')
    performing_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='votes_received')
    
    # Scoring criteria (1-10 scale)
    skill_score = models.PositiveIntegerField(null=True, blank=True, help_text="Skill/Technique (1-10)")
    creativity_score = models.PositiveIntegerField(null=True, blank=True, help_text="Creativity/Originality (1-10)")
    presentation_score = models.PositiveIntegerField(null=True, blank=True, help_text="Presentation/Stage Presence (1-10)")
    overall_score = models.PositiveIntegerField(null=True, blank=True, help_text="Overall Performance (1-10)")
    
    comments = models.TextField(blank=True, help_text="Optional feedback")
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'voting_player', 'performing_player']
    
    def __str__(self):
        return f"{self.voting_player.name} votes for {self.performing_player.name} - {self.event.name}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.voting_player == self.performing_player:
            raise ValidationError("Players cannot vote for themselves")
        # Prevent team members from voting for each other
        if self.voting_player.team == self.performing_player.team and self.voting_player.team != 'unassigned':
            raise ValidationError("Team members cannot vote for each other")
        
        # Ensure all scores are provided when saving
        if self.pk:  # Only validate on save, not initial form load
            score_fields = [self.skill_score, self.creativity_score, self.presentation_score, self.overall_score]
            if any(score is None for score in score_fields):
                raise ValidationError("All score fields must be provided")
            if any(score < 1 or score > 10 for score in score_fields if score is not None):
                raise ValidationError("All scores must be between 1 and 10")
    
    @property
    def total_score(self):
        scores = [
            self.skill_score or 0,
            self.creativity_score or 0, 
            self.presentation_score or 0,
            self.overall_score or 0
        ]
        return sum(scores)
    
    @property
    def average_score(self):
        total = self.total_score
        return total / 4 if total > 0 else 0


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
    points_per_participant = models.DecimalField(max_digits=5, decimal_places=2, default=0, 
                                               help_text="Points awarded per participating player")
    auto_calculate_points = models.BooleanField(default=False, 
                                              help_text="Automatically calculate total points based on participants")
    notes = models.TextField(blank=True, help_text="Optional notes about the scoring")
    awarded_by = models.CharField(max_length=100, help_text="Admin who awarded the points")
    awarded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'team']
        ordering = ['-points', 'team']
    
    def save(self, *args, **kwargs):
        """Auto-calculate points if enabled and update participant scores"""
        if self.auto_calculate_points and self.points_per_participant > 0:
            participant_count = self.get_participants().count()
            self.points = self.points_per_participant * participant_count
        
        super().save(*args, **kwargs)
        
        # Update individual player scores for participants
        self.update_participant_scores()
    
    def update_participant_scores(self):
        """Update individual scores for players who participated in this team event"""
        if self.points <= 0:
            return
            
        participants = self.get_participants()
        if not participants.exists():
            return
            
        # Calculate individual points per participant
        individual_points = float(self.points) / participants.count() if participants.count() > 0 else 0
        
        for participation in participants:
            player = participation.player
            
            # Update player's total score including this team event contribution
            self.update_single_player_score(player, individual_points)
    
    def update_single_player_score(self, player, team_event_points):
        """Update a single player's total score including team event contributions"""
        from django.db.models import Sum
        
        # Get treasure hunt score
        treasure_hunt_score = PlayerAnswer.objects.filter(
            player=player, 
            is_correct=True
        ).aggregate(Sum('points_awarded'))['points_awarded__sum'] or 0
        
        # Get individual event scores
        individual_event_score = IndividualEventScore.objects.filter(
            player=player
        ).aggregate(Sum('points'))['points__sum'] or 0
        
        # Get team event contributions (this player's share of team events they participated in)
        team_event_total = 0
        for event_score in EventScore.objects.filter(team=player.team):
            participants = event_score.get_participants()
            if participants.filter(player=player).exists() and participants.count() > 0:
                team_event_total += float(event_score.points) / participants.count()
        
        # Update player's total score
        new_total = treasure_hunt_score + float(individual_event_score) + team_event_total
        player.score = new_total
        player.save(update_fields=['score'])
    
    def get_participants(self):
        """Get players who participated in this team event"""
        return TeamEventParticipation.objects.filter(
            event_score=self,
            participated=True
        ).select_related('player')
    
    @property
    def participant_count(self):
        """Get number of participating players"""
        return self.get_participants().count()
    
    @property 
    def participating_players(self):
        """Get list of participating player names"""
        return [p.player.name for p in self.get_participants()]
    
    def __str__(self):
        return f"{self.get_team_display()} - {self.event.name}: {self.points} pts"


class TeamEventParticipation(models.Model):
    """Track individual player participation in team events"""
    event_score = models.ForeignKey(EventScore, on_delete=models.CASCADE, related_name='participations')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    participated = models.BooleanField(default=False, help_text="Did this player participate?")
    notes = models.TextField(blank=True, help_text="Optional notes about participation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['event_score', 'player']
        ordering = ['player__name']
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure player is from the same team as the event score
        if self.player.team != self.event_score.team:
            raise ValidationError(f"Player {self.player.name} is not from {self.event_score.get_team_display()}")
    
    def save(self, *args, **kwargs):
        """Save participation and update player scores"""
        super().save(*args, **kwargs)
        
        # Trigger score update for the event score (which will update all participants)
        if self.event_score:
            self.event_score.update_participant_scores()
    
    def delete(self, *args, **kwargs):
        """Delete participation and update scores"""
        event_score = self.event_score
        super().delete(*args, **kwargs)
        
        # Update scores after deletion
        if event_score:
            event_score.update_participant_scores()
    
    def __str__(self):
        status = "✓" if self.participated else "✗"
        return f"{status} {self.player.name} - {self.event_score.event.name}"

