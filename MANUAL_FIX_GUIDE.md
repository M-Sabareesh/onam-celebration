# Manual Fix Guide for Database Migrations and Static Files

## Problem Summary
- **Database Error**: `column core_event.participation_type does not exist`
- **Static Files Error**: `Missing staticfiles manifest entry for 'images/Maveli.jpg'`

## Quick Fixes

### 1. Database Migration Fix

```bash
# Step 1: Navigate to project directory
cd "c:\Users\SMADAMBA\OneDrive - Volvo Cars\Documents\Testing\Test\onam-celebration\onam-celebration"

# Step 2: Activate virtual environment (if using)
.venv\Scripts\activate

# Step 3: Apply migrations in order
python manage.py migrate core 0009
python manage.py migrate core 0010
python manage.py migrate core 0011  
python manage.py migrate core 0012
python manage.py migrate

# Step 4: Verify database
python manage.py shell
>>> from apps.core.models import Event
>>> Event.objects.first().participation_type  # Should not error
>>> exit()
```

### 2. Static Files Fix

```bash
# Step 1: Collect static files
python manage.py collectstatic --noinput

# Step 2: Copy Maveli images to static (if needed)
copy "media\Maveli\Maveli.jpg" "static\images\Maveli.jpg"
copy "media\Maveli\Maveli2.jpg" "static\images\Maveli2.jpg"
copy "media\Maveli\Maveli2.png" "static\images\Maveli2.png"
copy "media\Maveli\Maveli4.jpg" "static\images\Maveli4.jpg"

# Step 3: Re-collect static files
python manage.py collectstatic --noinput
```

### 3. Test Team Event Participation

```bash
# Start server
python manage.py runserver

# Open browser to: http://localhost:8000/admin
# Login and go to: Event Scores
# Create new score for a team event
# You should see participant checkboxes!
```

## Alternative: Reset and Re-apply Migrations

If the above doesn't work, try:

```bash
# Backup your data first!
python manage.py dumpdata core > backup.json

# Reset migrations (CAUTION: This will lose data!)
python manage.py migrate core zero
python manage.py migrate

# Restore data
python manage.py loaddata backup.json
```

## Features Available After Fix

✅ **Team Event Participation System**
- Admin can select which players participated using checkboxes
- Points auto-calculate based on: `participants × points_per_participant`
- Live preview of calculated points in admin
- Example: 5 players × 10 points = 50 total points

✅ **Enhanced Admin Interface**
- TeamEventParticipationInline shows team members
- Auto-calculation toggle
- Participant count display
- Select all/deselect all JavaScript helpers

✅ **Malayalam Branding**
- Site name: "ഓണാഘോഷം" (Onam Celebration)
- Maveli images throughout the site
- Noto Sans Malayalam font

## Verification Steps

1. **Check Database**: No more `participation_type` errors
2. **Check Static Files**: Maveli images load correctly
3. **Check Admin**: Event Scores show participant checkboxes
4. **Check Auto-calculation**: Points update when selecting participants
5. **Check Frontend**: Malayalam branding displays correctly

## Files Created/Modified

- `complete_fix_script.py` - Automated fix script
- `fix_database_migrations.py` - Database-specific fixes
- `fix_static_files.py` - Static files fixes
- Migration files: 0010, 0011, 0012 - Add new models and fields

## Support

If issues persist:
1. Check Django logs for specific errors
2. Verify virtual environment is activated
3. Ensure all required packages are installed
4. Try the manual migration steps above
