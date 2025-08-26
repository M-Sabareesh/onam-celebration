# Individual Event Scoring System - ഓണാഘോഷം

## Overview

The Onam celebration website now supports **individual event scoring** alongside team events. Individual players can participate in events and earn points that contribute to both their personal rankings and their team's overall score.

## Key Features

### 1. Event Types
Events now support three participation types:
- **Team Events**: Only teams can participate (e.g., Group Dance, Team Song)
- **Individual Events**: Only individual players participate (e.g., Solo Dance, Individual Art)
- **Mixed Events**: Support both team and individual participation (e.g., Quiz Competition)

### 2. Individual Event Scoring
- Individual players earn points for their performance in individual events
- These points are automatically converted to team points using a configurable multiplier
- Players' individual scores contribute to their personal ranking
- Team points from individual events contribute to team rankings

### 3. Point Multiplier System
Each event has an `individual_points_multiplier` setting:
- **1.0** = Individual points fully contribute to team (100%)
- **0.5** = Individual points contribute 50% to team
- **0.8** = Individual points contribute 80% to team
- This allows fine-tuning of how much individual performance affects team scores

## Models

### IndividualParticipation
Tracks which players are registered for individual events:
```python
class IndividualParticipation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
```

### IndividualEventScore
Stores scores for individual player performances:
```python
class IndividualEventScore(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    team_points = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Auto-calculated
    notes = models.TextField(blank=True)
    awarded_by = models.CharField(max_length=100)
    awarded_at = models.DateTimeField(auto_now_add=True)
```

### IndividualEventVote
Allows players to vote for individual performances:
```python
class IndividualEventVote(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    voting_player = models.ForeignKey(Player, related_name='votes_given')
    performing_player = models.ForeignKey(Player, related_name='votes_received')
    skill_score = models.PositiveIntegerField(help_text="Skill/Technique (1-10)")
    creativity_score = models.PositiveIntegerField(help_text="Creativity/Originality (1-10)")
    presentation_score = models.PositiveIntegerField(help_text="Presentation/Stage Presence (1-10)")
    overall_score = models.PositiveIntegerField(help_text="Overall Performance (1-10)")
    comments = models.TextField(blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)
```

## Admin Interface

### Event Management
- Create events with participation type selection
- Set individual points multiplier for each event
- Enable/disable voting for events

### Individual Event Score Admin
- Award points to individual players
- View auto-calculated team point contributions
- Add notes explaining scoring decisions
- Filter by event, player team, and date

### Individual Participation Admin
- Register players for individual events
- View participation history
- Filter events by participation type

### Individual Voting Admin
- Manage player votes for individual performances
- Validate voting scores (1-10 scale)
- Prevent self-voting and team-member voting

## Leaderboard Integration

### Team Standings
Team scores now include:
1. **Treasure Hunt Points**: Sum of all team members' treasure hunt scores
2. **Team Event Points**: Points from team-only events (voting + admin scores)
3. **Individual Event Points**: Sum of team_points from all team members' individual event scores

### Individual Rankings
- Players ranked by total individual points (treasure hunt + individual events)
- Individual event scores displayed separately from treasure hunt scores
- Top individual performers highlighted across all events

### Event Results Display
- Team events show traditional team voting/scoring results
- Individual events show top individual performers
- Mixed events display both team and individual results

## Usage Workflow

### For Admins

1. **Create Events**:
   ```
   Admin Panel → Events → Add Event
   - Set participation_type (team/individual/both)
   - Set individual_points_multiplier (0.1 to 1.0)
   - Enable voting if desired
   ```

2. **Register Individual Participants**:
   ```
   Admin Panel → Individual Participations → Add Individual Participation
   - Select event (filtered to individual/both events)
   - Select player
   ```

3. **Award Individual Scores**:
   ```
   Admin Panel → Individual Event Scores → Add Individual Event Score
   - Select event and player
   - Enter points (auto-calculates team_points)
   - Add notes explaining scoring
   ```

4. **Manage Voting**:
   ```
   Admin Panel → Individual Event Votes → Add Individual Event Vote
   - Select event, voting player, performing player
   - Rate skill, creativity, presentation, overall (1-10 each)
   - Add optional comments
   ```

### For Players

1. **Participate in Individual Events**:
   - Check leaderboard for available individual events
   - Register participation (through admin or future player interface)
   - Perform in the event

2. **Vote for Individual Performances**:
   - Rate other players' performances (not team members)
   - Use 1-10 scale for each criteria
   - Add constructive feedback

3. **View Results**:
   - Check individual rankings on leaderboard
   - See how individual performance contributes to team score
   - View top performers across all events

## Example Event Setup

### Individual Dance Competition
```python
Event.objects.create(
    name="Individual Classical Dance",
    event_type="individual_dance",
    participation_type="individual",
    individual_points_multiplier=0.6,  # 60% to team
    voting_enabled=True,
    description="Individual classical Kerala dance performance"
)
```

### Mixed Quiz Event
```python
Event.objects.create(
    name="Onam Knowledge Quiz",
    event_type="individual_quiz", 
    participation_type="both",  # Both team and individual
    individual_points_multiplier=0.8,  # 80% to team
    voting_enabled=False,  # Admin-scored only
    description="Individual quiz participation, scores contribute to team"
)
```

## Score Calculation Examples

### Individual Event Score: 85 points
- **Player gets**: 85 individual points
- **Team gets**: 85 × 0.6 = 51 team points (if multiplier is 0.6)

### Team Standing Calculation
```
Team Total Score = 
  Treasure Hunt Score + 
  Team Event Score + 
  Individual Event Team Points

Example:
  Treasure Hunt: 450 points
  Team Events: 75 points  
  Individual Events: 120 points (from all team members)
  Total: 645 points
```

## Future Enhancements

1. **Player Self-Registration**: Allow players to register for individual events
2. **Real-time Voting**: Live voting interface during events
3. **Performance Analytics**: Detailed statistics and trends
4. **Achievement Badges**: Individual achievement system
5. **Photo/Video Uploads**: Document individual performances
6. **Peer Reviews**: Extended feedback system

## Testing

Use the provided script to create sample data:
```bash
python create_sample_individual_events.py
```

This creates:
- Sample individual, team, and mixed events
- Individual participations for active players
- Sample individual event scores
- Demonstrates the complete individual scoring workflow

## Benefits

1. **Enhanced Engagement**: Individual recognition alongside team competition
2. **Flexible Scoring**: Configurable contribution of individual performance to team scores
3. **Fair Competition**: Separate individual and team rankings
4. **Comprehensive Tracking**: Complete performance history for all participants
5. **Admin Control**: Full administrative control over scoring and participation
