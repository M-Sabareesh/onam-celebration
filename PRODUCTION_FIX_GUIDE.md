# Production Database Fix Guide for Render Deployment

## 🚨 Current Issue
Your production server is failing with:
```
django.db.utils.ProgrammingError: column core_event.participation_type does not exist
```

This means the database migrations haven't been applied to your production PostgreSQL database.

## 🔧 Quick Fix Options

### Option 1: Django Management Command (Recommended)
```bash
# In your Render terminal or deployment script
python manage.py fix_database_schema

# To see what would be done first:
python manage.py fix_database_schema --dry-run
```

### Option 2: Manual Migration Commands
```bash
# Apply specific migrations in order
python manage.py migrate core 0010
python manage.py migrate core 0011
python manage.py migrate core 0012
python manage.py migrate
```

### Option 3: Emergency Python Script
```bash
# If migrations fail, run the emergency fix
python emergency_db_fix.py
```

## 📋 What These Fixes Do

### Database Changes Applied:
1. **Add `participation_type` column to Event table**
   - Allows events to be 'team', 'individual', or 'both'
   - Default: 'team' (backward compatible)

2. **Add `individual_points_multiplier` column to Event table**
   - Multiplier for individual points that go to team
   - Default: 1.0

3. **Add EventScore participation fields:**
   - `points_per_participant` - Points awarded per participating player
   - `auto_calculate_points` - Enable auto-calculation toggle

4. **Create TeamEventParticipation table:**
   - Track which players participated in team events
   - Enable checkbox selection in admin
   - Support for participation-based scoring

## 🎯 Expected Results After Fix

### ✅ Team Event Participation System
- **Admin Interface**: EventScore shows participant checkboxes
- **Auto-Calculation**: Points = participants × points_per_participant
- **Example**: 5 players × 10 points = 50 total points

### ✅ Enhanced Features
- Malayalam branding: "ഓണാഘോഷം" 
- Maveli images throughout site
- Dramatic leaderboard reveals
- Individual and team event scoring

## 🚀 Render Deployment Steps

### 1. Apply the Fix
Add to your `build.sh` or deployment script:
```bash
#!/bin/bash
# Build script for Render

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply database fixes
python manage.py fix_database_schema

# Apply any additional migrations
python manage.py migrate
```

### 2. Or Run Manually in Render Shell
```bash
# Connect to your Render shell and run:
python manage.py fix_database_schema
python manage.py migrate
```

### 3. Environment Variables
Ensure these are set in Render:
```
DJANGO_SETTINGS_MODULE=onam_project.settings.production
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=your-app.onrender.com
DEBUG=False
```

## 🔍 Verification Steps

### 1. Check Database Schema
```python
# In Django shell
from apps.core.models import Event, TeamEventParticipation

# This should not error
event = Event.objects.first()
print(event.participation_type)  # Should show 'team', 'individual', or 'both'

# This should not error  
TeamEventParticipation.objects.count()  # Should show 0 or number of records
```

### 2. Test Admin Interface
1. Go to `/custom-admin/`
2. Navigate to "Event Scores"
3. Create/edit a team event score
4. You should see participant checkboxes!

### 3. Test Auto-Calculation
1. Set "Points per participant" = 10
2. Enable "Auto calculate points"
3. Check 5 participant boxes
4. Points should auto-calculate to 50

## 🎉 Features Available After Fix

### Team Event Participation
- ✅ Checkbox selection of team members
- ✅ Auto-calculation: participants × points_per_participant
- ✅ Enhanced admin interface
- ✅ Live point calculation preview

### Malayalam Branding
- ✅ Site name: "ഓണാഘോഷം"
- ✅ Maveli images in navbar, home, about, footer
- ✅ Noto Sans Malayalam font

### Leaderboard System
- ✅ Dramatic reveal animations
- ✅ Team and individual results
- ✅ Confetti effects and podiums

## 🆘 If Issues Persist

### Check Logs
```bash
# In Render dashboard, check application logs for:
- Migration errors
- Database connection issues
- Static file problems
```

### Manual SQL Fix (Last Resort)
If all else fails, run this SQL directly in your PostgreSQL database:
```sql
-- Add missing columns
ALTER TABLE core_event ADD COLUMN participation_type VARCHAR(20) DEFAULT 'team';
ALTER TABLE core_event ADD COLUMN individual_points_multiplier DECIMAL(5,2) DEFAULT 1.0;
ALTER TABLE core_eventscore ADD COLUMN points_per_participant DECIMAL(5,2) DEFAULT 0;
ALTER TABLE core_eventscore ADD COLUMN auto_calculate_points BOOLEAN DEFAULT FALSE;

-- Create TeamEventParticipation table
CREATE TABLE core_teameventparticipation (
    id BIGSERIAL PRIMARY KEY,
    event_score_id BIGINT NOT NULL REFERENCES core_eventscore(id),
    player_id BIGINT NOT NULL REFERENCES core_player(id),
    participated BOOLEAN DEFAULT FALSE,
    notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(event_score_id, player_id)
);
```

## 📞 Support
- All fix scripts are in your project directory
- Migration files: 0010, 0011, 0012 contain the schema changes
- Documentation: `TEAM_PARTICIPATION_COMPLETE_GUIDE.md`

Your team event participation system is fully implemented and ready to use once the database schema is updated!
