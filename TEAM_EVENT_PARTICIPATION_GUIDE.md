# Team Event Participation Tracking System - ഓണാഘോഷം

## Overview

The Onam celebration website now supports **individual player participation tracking for team events**. This system allows administrators to:

- **Track which specific players participated** in each team event
- **Calculate points automatically** based on the number of participants
- **Award bonus points** for higher participation rates
- **Maintain flexible scoring** with manual override options

## Key Features

### 1. Individual Participation in Team Events
- **Checkbox selection** for each team member's participation
- **Automatic team filtering** - only show players from the selected team
- **Participation rate tracking** and reporting
- **Notes** for special participation circumstances

### 2. Flexible Point Calculation
- **Auto-calculation mode**: Points = Participants × Points per participant
- **Manual mode**: Fixed points regardless of participation count
- **Easy switching** between calculation modes
- **Real-time point updates** when participation changes

### 3. Enhanced Admin Interface
- **Inline participant selection** within event score forms
- **Visual participation indicators** (✓/✗ status)
- **Participation count display** in list views
- **Team-filtered player selection** for easy management

## Models

### Enhanced EventScore Model
```python
class EventScore(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    points_per_participant = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    auto_calculate_points = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    awarded_by = models.CharField(max_length=100)
    awarded_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def participant_count(self):
        return self.get_participants().count()
    
    def save(self, *args, **kwargs):
        # Auto-calculate points if enabled
        if self.auto_calculate_points and self.points_per_participant > 0:
            participant_count = self.get_participants().count()
            self.points = self.points_per_participant * participant_count
        super().save(*args, **kwargs)
```

### New TeamEventParticipation Model
```python
class TeamEventParticipation(models.Model):
    event_score = models.ForeignKey(EventScore, on_delete=models.CASCADE, related_name='participations')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    participated = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        # Ensure player is from the same team as the event score
        if self.player.team != self.event_score.team:
            raise ValidationError(f"Player {self.player.name} is not from {self.event_score.get_team_display()}")
```

## Admin Interface Workflow

### 1. Creating Team Event Scores

1. **Navigate to Event Scores** in admin panel
2. **Select event and team** for scoring
3. **Choose calculation mode**:
   - **Auto-calculate**: Enable checkbox and set points per participant
   - **Manual**: Disable checkbox and enter fixed points

### 2. Managing Participant Selection

1. **In the Event Score form**, scroll to "Team event participations" section
2. **Check/uncheck participation** for each team member
3. **Add notes** for special circumstances (optional)
4. **Save** - points auto-update if auto-calculation is enabled

### 3. Viewing Participation Data

- **List view** shows participant count for each event score
- **Detail view** shows all participants with status indicators
- **Team participation rates** displayed in summary views

## Usage Examples

### Example 1: Group Dance Event
```
Event: Thiruvathira Group Dance
Team: Team 1
Points per participant: 12
Participants: 4 players (checked)
Auto-calculated points: 4 × 12 = 48 points
```

### Example 2: Team Song with Manual Scoring
```
Event: Malayalam Song Competition  
Team: Team 2
Manual points: 65 (fixed)
Participants: 3 players (for tracking only)
Final points: 65 (manual override)
```

### Example 3: High Participation Bonus
```
Event: Pookalam Competition
Team: Team 3
Points per participant: 8
Participants: 6 out of 6 team members (100% participation)
Auto-calculated points: 6 × 8 = 48 points
Participation rate: 100% (bonus achievement!)
```

## Benefits of the System

### 1. **Fair Scoring**
- Points reflect actual team effort and participation
- Higher participation = higher potential scores
- Encourages full team involvement

### 2. **Accurate Tracking**
- Know exactly who participated in each event
- Historical participation records
- Team engagement analytics

### 3. **Flexible Management**
- Switch between auto and manual calculation as needed
- Handle special cases with notes and overrides
- Accommodate different event types and scoring rules

### 4. **Enhanced Competition**
- Teams motivated to maximize participation
- Clear correlation between effort and reward
- Transparent scoring based on actual involvement

## Scoring Strategies

### Strategy 1: Equal Points Per Person
```
Base points per participant: 10
Small team (3 participants): 30 points
Large team (6 participants): 60 points
Encourages maximum participation
```

### Strategy 2: Diminishing Returns
```
1st participant: 20 points
2nd participant: 15 points  
3rd participant: 10 points
4th+ participants: 5 points each
Balances small vs large teams
```

### Strategy 3: Participation Threshold
```
Minimum 3 participants required
Base: 30 points for 3 participants
Bonus: +8 points for each additional participant
Ensures minimum team effort while rewarding extra participation
```

## Admin Interface Features

### EventScore Admin Enhancements
- **Participant count column** in list view
- **Auto-calculation indicator** showing calculation mode
- **Inline participant management** with checkboxes
- **Real-time point calculation** updates
- **Team-filtered player selection** for easy management

### TeamEventParticipation Admin
- **Standalone participation management** for bulk operations
- **Participation status filtering** (participated/not participated)
- **Event and team filtering** for easy navigation
- **Participation timeline** with created/updated dates

### Enhanced List Displays
```
Event Score List:
[Event] [Team] [Points] [Participants] [Auto-Calc] [Awarded By] [Date]

Participation List:
[✓/✗] [Player] [Event] [Team] [Date] [Notes]
```

## API Integration

The system provides easy access to participation data:

```python
# Get participants for an event score
event_score = EventScore.objects.get(id=1)
participants = event_score.get_participants()
participant_names = event_score.participating_players

# Get participation rate
total_eligible = event_score.participations.count()
participated = event_score.participations.filter(participated=True).count()
participation_rate = (participated / total_eligible) * 100

# Auto-calculate points
event_score.points_per_participant = 10
event_score.auto_calculate_points = True
event_score.save()  # Points automatically calculated
```

## Migration and Setup

### Required Migration
Run migration `0012_team_event_participation.py` to:
- Add `points_per_participant` and `auto_calculate_points` fields to EventScore
- Create `TeamEventParticipation` model with proper relationships
- Set up constraints and indexes for optimal performance

### Automatic Setup
When creating an EventScore:
1. **Participation records auto-created** for all active team members
2. **Default participation status**: False (unchecked)
3. **Easy bulk selection** through admin interface

## Testing

Use the provided demo script:
```bash
python team_event_participation_demo.py
```

This demonstrates:
- Creating team events with participation tracking
- Auto vs manual point calculation examples
- Participation rate analysis
- Different scoring scenarios

## Future Enhancements

1. **Participation Trends**: Track player participation across multiple events
2. **Team Analytics**: Compare participation rates between teams
3. **Participation Rewards**: Bonus points for consistent participation
4. **Mobile Interface**: Easy participation marking during events
5. **Photo Documentation**: Link participation records to event photos

This system makes team event scoring more accurate, fair, and engaging by tracking actual individual participation while maintaining administrative flexibility!
