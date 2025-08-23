# ADMIN EVENT SCORING SYSTEM - IMPLEMENTATION GUIDE

## Overview
Comprehensive admin interface for creating events and awarding points directly to teams, with automatic leaderboard integration.

## Features Implemented

### 1. EventScore Model (`apps/core/models.py`)
```python
class EventScore(models.Model):
    """Admin-awarded scores for events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    awarded_by = models.CharField(max_length=100)
    awarded_at = models.DateTimeField(auto_now_add=True)
```

**Key Features:**
- Decimal points support (e.g., 8.5 points)
- Notes field for scoring transparency
- Tracks who awarded the points
- Automatic timestamp
- Unique constraint per event-team combination

### 2. Enhanced Event Model
**Updated `average_scores` property** to prioritize admin scores:
- If admin score exists: Use admin score
- If no admin score: Use voting average
- Provides both admin and voting scores in context

### 3. Admin Interface Enhancements

#### A. Event Management Page (`/admin/manage-events/`)
**Features:**
- Create new events with type, description, voting settings
- View all existing events with status
- Add teams to events
- Quick access to event scoring
- Direct links to edit events

**Event Creation:**
- Event name and type selection
- Optional description
- Enable/disable voting
- Automatic team participation management

#### B. Event Scoring Page (`/admin/event-scoring/<event_id>/`)
**Features:**
- Award points to any team (0-100 points, decimal allowed)
- Optional notes for transparency
- View current team scores
- See voting results (if enabled)
- Edit existing scores
- Automatic admin user tracking

#### C. Enhanced Admin Dashboard
**New sections:**
- Event Management quick links
- Event scoring access
- Event statistics

### 4. Admin Classes

#### EventScoreAdmin
- List view with points, team, event, awarded by
- Filterable by event, team, date
- Automatic admin user assignment
- Notes preview in list view

#### Updated EventAdmin
- Enhanced display with participation counts
- Bulk actions for voting enable/disable
- Team participation management
- Quick links to scoring pages

### 5. Template System

#### Manage Events Template (`templates/admin/manage_events.html`)
- Clean interface for event creation
- Event listing with status indicators
- Team participation management
- Quick action buttons

#### Event Scoring Template (`templates/admin/event_scoring.html`)
- Point award form with validation
- Current scores table
- Voting results display
- Breadcrumb navigation

## Usage Instructions

### For Administrators

#### 1. Create Events
```
1. Go to Admin → Manage Events
2. Fill in event details:
   - Name: "Group Dance Competition"
   - Type: "Group Dance"
   - Description: "Traditional Onam dance competition"
   - Voting: Enable if teams should vote for each other
3. Click "Create Event"
```

#### 2. Add Teams to Events
```
1. In the event list, find your event
2. Use "Add Team to Event" dropdown
3. Select team and click "Add Team"
4. Repeat for all participating teams
```

#### 3. Award Points
```
1. Click "Manage Scores" for an event
2. Select team from dropdown
3. Enter points (can be decimal: 8.5)
4. Add optional notes about the scoring
5. Click "Award Points"
```

#### 4. Update Scores
```
1. From event scoring page, click "Edit" next to any score
2. Modify points or notes
3. Save changes
4. Points automatically update in leaderboard
```

### For Users

#### Leaderboard Integration
- Team standings show combined treasure hunt + event scores
- Event-specific results section displays all event scores
- Score breakdown shows treasure hunt vs event points
- Real-time updates when admin awards points

## Technical Implementation

### Score Priority Logic
```python
# In Event.average_scores property
admin_score = EventScore.objects.get(event=self, team=team_code).points
voting_score = calculate_voting_average()

# Admin score takes priority
final_score = admin_score if admin_score > 0 else voting_score
```

### Leaderboard Integration
```python
# In LeaderboardView
for event in active_events:
    event_scores = event.average_scores  # Uses admin scores if available
    team_data[team_code]['event_scores'][event.name] = score
    team_data[team_code]['total_event_score'] += score

# Final total
team_data[team_code]['total_score'] = (
    treasure_hunt_score + total_event_score
)
```

### Database Structure
```sql
-- EventScore table
CREATE TABLE core_eventscore (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES core_event(id),
    team VARCHAR(20),
    points DECIMAL(5,2),
    notes TEXT,
    awarded_by VARCHAR(100),
    awarded_at TIMESTAMP,
    UNIQUE(event_id, team)
);
```

## Admin Workflow Examples

### Example 1: Group Dance Competition
```
1. Create Event:
   - Name: "Group Dance Competition"
   - Type: "Group Dance" 
   - Voting: Disabled (admin will score directly)

2. Add Teams:
   - Add all 4 teams to the event

3. Award Points After Performance:
   - Team 1: 8.5 points - "Excellent coordination"
   - Team 2: 7.8 points - "Good performance, minor timing issues"
   - Team 3: 9.2 points - "Outstanding synchronization"
   - Team 4: 8.0 points - "Creative choreography"

4. Results:
   - Automatically appear in leaderboard
   - Teams ranked by combined treasure hunt + event scores
```

### Example 2: Cultural Event with Voting
```
1. Create Event:
   - Name: "Cultural Performance"
   - Type: "Group Dance"
   - Voting: Enabled (teams vote for each other)

2. During Event:
   - Teams vote using existing voting system
   - Average scores calculated automatically

3. Admin Override (if needed):
   - Admin can award official scores
   - Admin scores override voting results
   - Maintains transparency with notes
```

## Benefits

### For Administrators
- **Full Control**: Direct point assignment with decimal precision
- **Transparency**: Notes field explains scoring decisions
- **Flexibility**: Can override voting results when needed
- **Audit Trail**: Tracks who awarded points and when
- **Integration**: Automatic leaderboard updates

### For Participants
- **Clear Scoring**: See exact points for each event
- **Transparency**: Admin notes explain scoring
- **Fair Competition**: Consistent scoring across events
- **Real-time Updates**: Immediate leaderboard reflection

### For Event Management
- **Scalability**: Unlimited events and scoring
- **Flexibility**: Mix of voting and admin-scored events
- **Efficiency**: Quick point assignment interface
- **Reporting**: Complete score history and notes

## Security Features

### Access Control
- Only admin users can access scoring pages
- Staff member required decorators on all admin views
- CSRF protection on all forms

### Data Integrity
- Unique constraints prevent duplicate scores
- Decimal validation for point values
- Team choice validation
- Automatic timestamp recording

## Testing

### Test Script: `test_admin_event_scoring.py`
- Creates sample events and scores
- Tests leaderboard integration
- Validates score priority logic
- Provides usage instructions

### Manual Testing Checklist
- [ ] Create events through admin interface
- [ ] Add teams to events
- [ ] Award points with decimal values
- [ ] Update existing scores
- [ ] Verify leaderboard integration
- [ ] Test voting override functionality
- [ ] Check admin notes display

## Migration

### Database Changes
```bash
python manage.py makemigrations core  # Creates EventScore migration
python manage.py migrate              # Applies the migration
```

### Existing Data
- No impact on existing events or votes
- New EventScore model works alongside existing voting
- Admin scores take priority when both exist

## Future Enhancements

### Potential Additions
1. **Bulk Scoring**: Upload CSV with multiple team scores
2. **Score Categories**: Different point categories per event
3. **Score Templates**: Predefined scoring criteria
4. **Approval Workflow**: Multi-admin score approval
5. **Historical Reports**: Score change history and analytics
6. **Mobile Interface**: Mobile-optimized admin scoring

### Integration Opportunities
1. **Real-time Notifications**: Alert teams when scores are awarded
2. **API Endpoints**: External scoring system integration
3. **Analytics Dashboard**: Score distribution and trends
4. **Export Features**: PDF reports and CSV exports

## Conclusion

The Admin Event Scoring System provides a comprehensive, flexible, and transparent way to manage event competitions within the Onam Aghosham celebration. It seamlessly integrates with the existing leaderboard while giving administrators full control over event scoring and team performance evaluation.

The system maintains the existing voting functionality while providing admin override capabilities, ensuring fair and accurate competition results that reflect both peer evaluation and official judging standards.
