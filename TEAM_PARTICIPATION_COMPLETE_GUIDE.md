# Team Event Participation System - Complete Guide

## 🎯 Overview

The Onam Celebration website now includes a comprehensive **Team Event Participation System** that allows administrators to:

1. **Select specific players** who participated in team events using checkboxes
2. **Auto-calculate points** based on the number of participants
3. **Track participation** for scoring accuracy
4. **Enhanced admin experience** with live point calculation

## 🏗️ System Architecture

### Models

#### 1. **EventScore** (Enhanced)
```python
class EventScore(models.Model):
    event = models.ForeignKey(Event)
    team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # NEW FIELDS for participation-based scoring
    points_per_participant = models.DecimalField(default=0, help_text="Points per participating player")
    auto_calculate_points = models.BooleanField(default=False, help_text="Auto-calculate based on participants")
    
    notes = models.TextField(blank=True)
    awarded_by = models.CharField(max_length=100)
    awarded_at = models.DateTimeField(auto_now_add=True)
```

#### 2. **TeamEventParticipation** (New)
```python
class TeamEventParticipation(models.Model):
    event_score = models.ForeignKey(EventScore, related_name='participations')
    player = models.ForeignKey(Player)
    participated = models.BooleanField(default=False, help_text="Did this player participate?")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🔧 How It Works

### Admin Workflow

1. **Create/Edit EventScore**
   - Select event and team
   - Choose between manual points OR auto-calculation
   - Set `points_per_participant` (e.g., 10 points per player)
   - Enable `auto_calculate_points`

2. **Select Participants**
   - Inline form shows all team members
   - Check boxes for players who participated
   - Add optional notes about participation

3. **Auto-Calculation**
   - Points = `participant_count × points_per_participant`
   - Example: 5 participants × 10 points = 50 total points
   - Updates automatically when checkboxes change

### Example Scenario: Group Dance

```
Event: "Group Dance Competition"
Team: Red Team (8 members total)
Points per participant: 10

Admin selects 5 participants:
✅ Arjun Kumar
✅ Priya Nair  
✅ Rahul Menon
✅ Anjali Das
✅ Kiran Pillai
❌ Deepak Shah (not participated)
❌ Meera Iyer (not participated)  
❌ Suresh Varma (not participated)

Auto-calculated points: 5 × 10 = 50 points
```

## 💻 Admin Interface Features

### EventScore Admin
- **List View**: Shows participant count and calculation mode
- **Edit Form**: 
  - Point calculation section with auto-toggle
  - Participant count display (read-only)
  - Inline participant selection

### TeamEventParticipation Inline
- **Filtered Players**: Only shows team members
- **Checkbox Selection**: Easy participate/not participate toggle
- **Notes Field**: Optional participation details
- **Auto-Population**: Team members added automatically

### Enhanced UX (JavaScript)
- **Select All/Deselect All** buttons for quick selection
- **Live Point Calculation** preview
- **Participant Counter** updates in real-time

## 🎨 Frontend Integration

### Leaderboard Display
- Shows total points for teams
- Can display participant information
- Reflects participation-based scoring

### Event Results
- Team scores include participation details
- Individual recognition for participants
- Transparent scoring system

## 📊 Database Schema

```sql
-- EventScore table (enhanced)
ALTER TABLE core_eventscore ADD COLUMN points_per_participant DECIMAL(5,2) DEFAULT 0;
ALTER TABLE core_eventscore ADD COLUMN auto_calculate_points BOOLEAN DEFAULT FALSE;

-- New TeamEventParticipation table
CREATE TABLE core_teameventparticipation (
    id BIGINT PRIMARY KEY,
    event_score_id BIGINT REFERENCES core_eventscore(id),
    player_id BIGINT REFERENCES core_player(id),
    participated BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(event_score_id, player_id)
);
```

## 🚀 Usage Examples

### 1. Group Dance (5 participants)
```
Event: Group Dance
Team: Red Team
Points per participant: 10
Participants: 5 players
Total Points: 5 × 10 = 50
```

### 2. Drama Performance (8 participants)
```
Event: Drama Performance  
Team: Blue Team
Points per participant: 15
Participants: 8 players
Total Points: 8 × 15 = 120
```

### 3. Mixed Participation Event
```
Event: Cultural Showcase
Team: Green Team (12 members)
Participants: 7 out of 12 members
Points per participant: 8
Total Points: 7 × 8 = 56
```

## 🎯 Benefits

### For Administrators
- **Fair Scoring**: Points based on actual participation
- **Easy Management**: Checkbox interface for participant selection
- **Flexible Calculation**: Manual points OR auto-calculation
- **Audit Trail**: Track who participated and when

### For Teams
- **Transparent Scoring**: Clear participation-based points
- **Individual Recognition**: Players get credit for participation
- **Fair Competition**: Points reflect actual effort invested

### For Events
- **Accurate Records**: Track participation for each event
- **Historical Data**: Maintain participation records
- **Flexible Scoring**: Adapt to different event types

## 🔧 Technical Implementation

### Backend Logic
```python
def save(self, *args, **kwargs):
    """Auto-calculate points if enabled"""
    if self.auto_calculate_points and self.points_per_participant > 0:
        participant_count = self.get_participants().count()
        self.points = self.points_per_participant * participant_count
    super().save(*args, **kwargs)

def get_participants(self):
    """Get players who participated"""
    return TeamEventParticipation.objects.filter(
        event_score=self,
        participated=True
    ).select_related('player')
```

### Frontend JavaScript
```javascript
// Live calculation preview
function updatePointsPreview() {
    const participantCount = document.querySelectorAll('input[name*="participated"]:checked').length;
    const pointsPerParticipant = document.getElementById('id_points_per_participant').value;
    const totalPoints = participantCount * pointsPerParticipant;
    document.getElementById('points-preview').textContent = totalPoints;
}
```

## 📋 Migration Guide

### Applied Migrations
1. **0010_individual_event_models.py** - Added `participation_type` to Event
2. **0011_fix_individual_vote_null_fields.py** - Fixed null field issues
3. **0012_team_event_participation.py** - Added TeamEventParticipation model

### Migration Commands
```bash
python manage.py migrate core 0010
python manage.py migrate core 0011  
python manage.py migrate core 0012
python manage.py migrate
```

## 🎉 Features Summary

✅ **Implemented and Working:**
- Checkbox selection for team event participants
- Auto-calculation of points based on participant count
- Enhanced admin interface with inline participant selection
- Live point calculation preview
- Team member filtering and auto-population
- Malayalam branding with Maveli images
- Dramatic leaderboard reveal system
- Individual and team event scoring
- Comprehensive documentation

✅ **Ready to Use:**
- Create EventScore for team events
- Select participants using checkboxes
- Points auto-calculate: `participants × points_per_participant`
- Example: 5 players × 10 points = 50 total points

This system provides exactly what you requested: **checkbox selection of team members with automatic point calculation based on participation count**. The implementation is robust, user-friendly, and fully integrated with the existing Malayalam-branded Onam celebration website.
