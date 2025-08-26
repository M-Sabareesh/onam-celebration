# 🚨 PRODUCTION FIX - Leaderboard Error

## Error Message
```
django.db.utils.ProgrammingError: relation "core_individualeventscore" does not exist
```

## Quick Fix (Choose One Method)

### Method 1: Windows Batch Script (Easiest)
```cmd
cd path\to\your\onam-celebration\project
fix_production_migrations.bat
```

### Method 2: Linux/Mac Script  
```bash
cd path/to/your/onam-celebration/project
chmod +x fix_production_migrations.sh
./fix_production_migrations.sh
```

### Method 3: Manual Commands
```bash
python manage.py migrate core 0010
python manage.py migrate core 0011  
python manage.py migrate core 0012
python manage.py migrate
```

### Method 4: Python Script
```bash
python fix_leaderboard_production.py
```

## What This Fixes

✅ **Database Tables:** Creates missing tables for individual event scoring  
✅ **Leaderboard Error:** Fixes the "relation does not exist" error  
✅ **Malayalam Branding:** Enables "ഓണാഘോഷം" site title  
✅ **Maveli Images:** Shows Maveli images on all pages  
✅ **Individual Scoring:** Enables admin interface for individual event scoring  
✅ **Team Participation:** Tracks which players participate in team events  

## After Running The Fix

1. **Restart** your Django application
2. **Visit** `/leaderboard/` - should work without errors
3. **Check** `/admin/` - should have "Individual Event Scores" section
4. **Verify** Malayalam title "ഓണാഘോഷം" is visible
5. **Confirm** Maveli images appear on homepage

## If Fix Doesn't Work

1. Check you're in the correct project directory (where `manage.py` is)
2. Ensure virtual environment is activated
3. Run `python manage.py showmigrations core` to check status
4. Check Django logs for specific error messages

## Files This Creates/Fixes

- Database tables: `core_individualeventscore`, `core_individualparticipation`, etc.
- Migration files: Already exist in `apps/core/migrations/`
- No code changes needed - just database updates

## Support

If the automated scripts don't work, you can:
1. Run migrations manually (Method 3 above)
2. Check `PRODUCTION_MIGRATION_FIX_GUIDE.md` for detailed troubleshooting
3. Use the emergency script: `python emergency_leaderboard_fix.py`

---

**Note:** This only fixes the database issue. All the Malayalam branding, Maveli images, and enhanced scoring features are already implemented in the code.
