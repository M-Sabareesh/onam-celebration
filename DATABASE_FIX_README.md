# 🚨 Database Issue? Quick Fix!

If you're seeing errors about missing `core_teamconfiguration` table, here's how to fix it:

## 🔥 For Render.com Production

Update your **Start Command** in Render dashboard to:
```bash
python quick_fix.py && gunicorn onam_project.wsgi:application
```

## 💻 For Local Development

### Windows Users
```cmd
fix_database.bat
```

### All Users
```bash
python quick_fix.py
```

## 🎯 What This Fixes

- ✅ Creates missing `core_teamconfiguration` table
- ✅ Sets up default team names
- ✅ Creates admin user if needed
- ✅ Verifies database is ready

## 🏆 After Fix

- Site will be accessible
- Admin panel: `/admin/` (username: admin, password: admin123)
- Team names editable at: **Core > Team configurations**

## 🆘 Still Having Issues?

1. Check `URGENT_PRODUCTION_FIX.md`
2. Try `python direct_fix.py`
3. Run `python emergency_production_fix.py`

---
*This fix handles the missing TeamConfiguration table issue that prevents the Onam Celebration site from starting.*
