# Production Migration Fix Guide - Onam Celebration

## Problem Description
The leaderboard is showing the error: `no such table: core_individualeventscore` because the database migrations for the new individual event scoring system haven't been applied in production.

## Root Cause
New models were added for individual event scoring:
- `IndividualParticipation`
- `IndividualEventScore` 
- `IndividualEventVote`
- `TeamEventParticipation`

The corresponding database tables don't exist because migrations 0010, 0011, and 0012 haven't been applied.

## Quick Fix Solutions

### Option 1: Run the Automated Fix Script (Recommended)

**For Windows:**
```cmd
cd path\to\onam-celebration
fix_production_migrations.bat
```

**For Linux/Mac:**
```bash
cd path/to/onam-celebration
chmod +x fix_production_migrations.sh
./fix_production_migrations.sh
```

### Option 2: Manual Migration Commands

1. **Check current status:**
```bash
python manage.py showmigrations core
```

2. **Apply migrations in order:**
```bash
python manage.py migrate core 0010
python manage.py migrate core 0011  
python manage.py migrate core 0012
python manage.py migrate
```

3. **Verify tables exist:**
```bash
python manage.py shell
```
```python
from apps.core.models import IndividualEventScore, TeamEventParticipation
print("Tables created successfully!")
```

### Option 3: Emergency Leaderboard Fix (If migrations fail)

If migrations fail completely, use the emergency script:
```bash
python emergency_leaderboard_fix.py
```

This will disable individual scoring temporarily while maintaining basic leaderboard functionality.

## Verification Steps

After running the fix:

1. **Check migration status:**
```bash
python manage.py showmigrations core
```
All migrations should show `[X]`

2. **Test leaderboard:**
   - Visit `/leaderboard/` 
   - Should see Malayalam "ഓണാഘോഷം" branding
   - Should see Maveli images
   - Should see team scores without errors

3. **Test admin interface:**
   - Visit `/admin/`
   - Go to Core > Individual Event Scores
   - Should load without errors

## Migration Details

### Migration 0010: Individual Event Models
- Creates `IndividualParticipation` table
- Creates `IndividualEventScore` table  
- Creates `IndividualEventVote` table

### Migration 0011: Fix Individual Vote Null Fields
- Makes score fields nullable in `IndividualEventVote`
- Fixes TypeError in admin interface

### Migration 0012: Team Event Participation
- Creates `TeamEventParticipation` table
- Adds many-to-many relationship for team event participants

## Troubleshooting

### Issue: "No module named 'apps.core'"
**Solution:** Make sure you're in the project root directory where `manage.py` is located.

### Issue: "ImproperlyConfigured: The SECRET_KEY setting must not be empty"
**Solution:** Make sure your environment variables are set or create a `.env` file.

### Issue: Migration fails with "table already exists"
**Solution:** Use fake migration:
```bash
python manage.py migrate core 0010 --fake
python manage.py migrate core 0011 --fake
python manage.py migrate core 0012 --fake
```

### Issue: SQLite database is locked
**Solution:** 
1. Stop Django development server
2. Run migrations
3. Restart server

## Production Deployment Notes

### For Render/Heroku:
1. Push changes to git repository
2. Migrations will run automatically on deployment
3. Check deployment logs for migration status

### For VPS/Manual Deployment:
1. Pull latest code: `git pull origin main`
2. Run fix script: `./fix_production_migrations.sh`
3. Restart Django/gunicorn service

## Features Enabled After Fix

✅ **Malayalam Branding:** Site title shows "ഓണാഘോഷം"  
✅ **Maveli Images:** Visible on all pages with fallback emoji  
✅ **Individual Event Scoring:** Admin can score individual events  
✅ **Team Event Participation:** Track which players participate in team events  
✅ **Auto Point Calculation:** Points calculated based on participant count  
✅ **Dramatic Leaderboard:** Reveals scores with animations  
✅ **Robust Error Handling:** Graceful fallbacks if data is missing

## Files Created/Modified

### Migration Scripts:
- `fix_production_migrations.sh` - Linux/Mac script
- `fix_production_migrations.bat` - Windows script  
- `apply_migrations_production.py` - Python version
- `emergency_leaderboard_fix.py` - Emergency fallback

### Documentation:
- `PRODUCTION_MIGRATION_FIX_GUIDE.md` - This guide
- `INDIVIDUAL_EVENT_SCORING_GUIDE.md` - Individual scoring system
- `TEAM_EVENT_PARTICIPATION_GUIDE.md` - Team participation system

### Database Migrations:
- `apps/core/migrations/0010_individual_event_models.py`
- `apps/core/migrations/0011_fix_individual_vote_null_fields.py`  
- `apps/core/migrations/0012_team_event_participation.py`

## Contact/Support

If the automated fix doesn't work:
1. Check Django logs for specific error messages
2. Verify all migration files exist in `apps/core/migrations/`
3. Try the emergency leaderboard fix as a temporary solution
4. Consider manual database table creation if migrations repeatedly fail

The site should be fully functional with Malayalam branding, Maveli imagery, and complete scoring systems after applying these fixes.
