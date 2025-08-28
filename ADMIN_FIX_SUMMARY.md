# Admin Registration Fix - Summary

## Problem
The deployment was failing with this error:
```
django.contrib.admin.sites.AlreadyRegistered: The model SimpleEventScore is already registered with 'core.SimpleEventScoreAdmin'.
```

## Root Cause
The `SimpleEventScore` model was being registered with Django admin in two places:

1. **Decorator registration** (line 973): `@admin.register(SimpleEventScore)`
2. **Manual registration** (line 1027): `admin.site.register(SimpleEventScore, SimpleEventScoreAdmin)`

## Fix Applied
Removed the duplicate manual registration on line 1027 in `apps/core/admin.py`:

**Before:**
```python
admin.site.register(IndividualEventScore, IndividualEventScoreAdmin)
admin.site.register(IndividualEventVote, IndividualEventVoteAdmin)
admin.site.register(SimpleEventScore, SimpleEventScoreAdmin)  # ← REMOVED THIS LINE
```

**After:**
```python
admin.site.register(IndividualEventScore, IndividualEventScoreAdmin)
admin.site.register(IndividualEventVote, IndividualEventVoteAdmin)
```

## Verification
The `SimpleEventScore` model is now only registered once via the decorator:
```python
@admin.register(SimpleEventScore)
class SimpleEventScoreAdmin(admin.ModelAdmin):
    ...
```

## Impact
## CRITICAL UPDATE - August 28, 2025

🚨 **EMERGENCY: Multiple missing database tables causing admin crashes**

### Missing Tables:
1. `core_simpleeventscore` - Main scoring table
2. `core_simpleeventscore_participants` - Many-to-many relationship table

### Current Errors:
- Admin scoring interface: 500 errors
- Player management interface: 500 errors
- Multiple admin sections affected

### IMMEDIATE ACTION REQUIRED:
**Run ONE of these commands to fix:**

```batch
# Option 1: Use the batch script
fix_table.bat

# Option 2: Use the Python emergency script
python EMERGENCY_FIX.py

# Option 3: Manual command
env\Scripts\activate
python manage.py migrate core --verbosity=2
```

### Root Cause:
Migration `0015_simple_event_scoring.py` not applied to production database.

---

## Previous Work Completed ✅
- ✅ Team filtering JavaScript rewritten and working
- ✅ Image display fixed and working
- ✅ Deployment error resolved
- ❌ **CRITICAL**: Database migration not applied

## Next Steps - URGENT
1. **IMMEDIATELY**: Run migration fix script to create missing tables
2. Restart Django application/web server
3. Test admin interface for 500 errors
4. Verify scoring workflow works
5. Test team filtering and image display

## 🚀 RENDER START COMMAND

For your Render deployment, use this as your **Start Command**:

```bash
python render_fix_start.py
```

**Alternative commands if the above fails:**

```bash
# Option 1: Direct migration + gunicorn
python manage.py migrate core --noinput && python manage.py collectstatic --noinput && gunicorn onam_project.wsgi:application --bind 0.0.0.0:$PORT

# Option 2: Manual migration fix first
python manage.py migrate core 0015 --verbosity=1 && python manage.py migrate --noinput && gunicorn onam_project.wsgi:application --bind 0.0.0.0:$PORT

# Option 3: Simple fallback
gunicorn onam_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1
```

### Environment Variables for Render:
```
DJANGO_SETTINGS_MODULE=onam_project.settings.production
PORT=10000
WEB_CONCURRENCY=1
```

### What the start script does:
1. ✅ Checks Redis availability
2. 🔧 **FIXES missing tables** (applies migration 0015)
3. 🔄 Runs all migrations
4. 📁 Collects static files
5. 📂 Creates media directories
6. ✅ Verifies tables exist
7. 🚀 Starts Gunicorn server
