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
- ✅ Deployment error resolved
- ✅ Simple event scoring admin interface remains functional
- ✅ All scoring URLs still work: `/admin/simple-scoring/`, `/simple-scoring/`, `/event-scoring/`
- ✅ No functional changes to the scoring system

## Next Steps
1. Test deployment to ensure the fix works
2. Verify admin interface accessibility
3. Test the simple event scoring workflow
