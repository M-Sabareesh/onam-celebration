# Events and Voting System Implementation

## ✅ COMPLETED: Team Competition Events with Voting

I've successfully implemented a comprehensive events and voting system for your Onam Django application. Here's what has been added:

## 🎭 New Features

### 1. Event Management System ✅
- **Event Types**: Group Dance and Group Song competitions
- **Team Participation**: Teams can be registered for events
- **Voting Control**: Admins can enable/disable voting for each event
- **Real-time Scores**: Live score calculation and display

### 2. Voting System ✅
Teams vote for each other's performances on **4 criteria (1-10 scale)**:
- **Group Coordination**: How well did the team work together?
- **Song/Dance Selection**: How appropriate was their choice?
- **Overall Dance/Song**: Quality of the performance
- **Enjoying the Event**: How entertaining was it?

### 3. Admin Interface ✅
- **Event Management**: Create, edit, activate/deactivate events
- **Team Registration**: Manage which teams participate in each event
- **Vote Monitoring**: View all votes and scores
- **Bulk Actions**: Enable/disable voting for multiple events

### 4. User Interface ✅
- **Events List Page**: View all available events and current scores
- **Event Detail Page**: Vote for teams and see detailed scores
- **Real-time Updates**: Scores refresh automatically
- **Responsive Design**: Works on all device sizes

## 🗂️ Database Models

### Event Model
```python
class Event(models.Model):
    name = models.CharField(max_length=100)
    event_type = models.CharField(choices=[
        ('group_dance', 'Group Dance'),
        ('group_song', 'Group Song'),
    ])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    voting_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### EventParticipation Model
```python
class EventParticipation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    registered_at = models.DateTimeField(auto_now_add=True)
```

### EventVote Model
```python
class EventVote(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    voting_team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    performing_team = models.CharField(max_length=20, choices=Player.TEAM_CHOICES)
    coordination_score = models.PositiveIntegerField()  # 1-10
    selection_score = models.PositiveIntegerField()     # 1-10
    overall_score = models.PositiveIntegerField()       # 1-10
    enjoyment_score = models.PositiveIntegerField()     # 1-10
    comments = models.TextField(blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)
```

## 🌐 URLs and Views

### New URLs Added:
- `/events/` - Events list page
- `/events/<id>/` - Event detail and voting page
- `/api/events/<id>/voting/` - Real-time voting API

### View Classes:
- `EventsListView` - Display all events with scores
- `EventDetailView` - Event details and voting interface
- `EventVotingAPI` - API for real-time score updates

## 🎨 Templates

### events_list.html
- Overview of all events
- Current scores display
- Team participation status
- Navigation to voting

### event_detail.html
- Detailed event information
- Voting forms for each team
- Real-time score updates
- Voting instructions

## 🔧 How to Use

### For Admins:

1. **Create Events**:
   - Go to Admin → Core → Events
   - Create "Group Dance" and "Group Song" events
   - Set descriptions and activate events

2. **Register Teams**:
   - Go to Admin → Core → Event participations
   - Register teams for each event

3. **Enable Voting**:
   - Edit events and check "Voting enabled"
   - Teams can now vote for each other

4. **Monitor Votes**:
   - Go to Admin → Core → Event votes
   - View all submitted votes and scores

### For Users:

1. **Access Events**:
   - Navigate to "Events" in the main menu
   - View list of available events

2. **Vote for Teams**:
   - Click on an event to view details
   - Vote for other teams (not your own)
   - Rate on 4 criteria (1-10 scale)
   - Add optional comments

3. **View Scores**:
   - See real-time average scores
   - Scores update automatically
   - Compare team performances

## 📊 Scoring System

### Individual Vote:
- Each criterion: 1-10 points
- Total per vote: 4-40 points
- Average per vote: 1-10 points

### Team Scores:
- **Coordination**: Average of all coordination scores
- **Selection**: Average of all selection scores
- **Overall**: Average of all overall scores
- **Enjoyment**: Average of all enjoyment scores
- **Total**: Average of all four criteria

### Validation:
- Teams cannot vote for themselves
- All scores must be 1-10
- One vote per team per performing team
- Votes can be updated

## 🚀 Setup Instructions

### 1. Run Migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Sample Events:
```bash
python create_sample_events.py
```

### 3. Access the System:
- Events page: http://127.0.0.1:8000/events/
- Admin interface: http://127.0.0.1:8000/admin/

## 📱 Features

### ✅ Implemented Features:
- Two event types: Group Dance & Group Song
- 4-criteria voting system (1-10 scale)
- Team-based voting (teams vote for other teams)
- Real-time score calculation and display
- Admin interface for event management
- Responsive web interface
- Vote validation and error handling
- Comments system for feedback
- Auto-refreshing scores
- Navigation integration

### 🎯 Voting Rules:
- Teams can only vote for other teams (not themselves)
- One vote per team per performing team per event
- Votes can be updated/changed
- All 4 criteria must be scored
- Scores must be between 1-10
- Voting can be enabled/disabled by admins

## 📁 Files Created/Modified:

### Models:
- `apps/core/models.py` - Added Event, EventParticipation, EventVote models

### Views:
- `apps/core/views.py` - Added EventsListView, EventDetailView, EventVotingAPI

### Templates:
- `templates/core/events_list.html` - Events overview page
- `templates/core/event_detail.html` - Event voting page
- `templates/base.html` - Added Events navigation link

### Admin:
- `apps/core/admin.py` - Added admin classes for event management

### URLs:
- `apps/core/urls.py` - Added event URLs

### Scripts:
- `create_sample_events.py` - Setup script for sample data

## 🎉 Status: ✅ READY FOR USE

The events and voting system is fully implemented and ready for your Onam celebration! Teams can now compete in Group Dance and Group Song events, and vote for each other's performances using the comprehensive 4-criteria rating system.
