# 🚨 EMERGENCY PRODUCTION FIX GUIDE
## Missing django_session Table Error

### Problem
Your production site is showing the error:
```
OperationalError: no such table: django_session
```

This means Django's core migrations haven't been applied to your production database.

### Quick Fix (Choose One Method)

#### Method 1: Run the Emergency Script
```bash
# In your production environment (Render, etc.)
python fix_production_database.py
```

#### Method 2: Manual Migration Steps
```bash
# 1. Apply core Django migrations first
python manage.py migrate contenttypes
python manage.py migrate auth
python manage.py migrate sessions
python manage.py migrate admin

# 2. Apply your app migrations
python manage.py migrate core
python manage.py migrate accounts
python manage.py migrate games

# 3. Apply all remaining migrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput
```

#### Method 3: For Render.com Deployment
1. Go to your Render dashboard
2. Find your web service
3. Go to "Settings" > "Environment Variables"
4. Add/verify these variables:
   ```
   DJANGO_SETTINGS_MODULE=onam_project.settings.production
   DJANGO_SUPERUSER_USERNAME=OnamAdmin
   DJANGO_SUPERUSER_PASSWORD=your_secure_password
   DJANGO_SUPERUSER_EMAIL=your_email@example.com
   ```
5. Go to "Manual Deploy" and click "Deploy Latest Commit"
6. Monitor the build logs to ensure migrations run successfully

### What This Fixes

1. **django_session table** - Enables user sessions and login functionality
2. **All Django core tables** - auth_user, django_admin_log, etc.
3. **Your app tables** - TeamConfiguration, Player, Event, etc.
4. **Static files** - CSS, JS, images properly collected
5. **Admin access** - Creates superuser for admin panel

### After Fix: Team Name Management

Once the fix is applied, you can manage team names through the Django admin:

1. Go to: `https://your-site.com/admin/`
2. Login with superuser credentials
3. Navigate to: **Core > Team configurations**
4. Edit team names:
   - Team 1 → "Red Warriors"
   - Team 2 → "Blue Champions"
   - Team 3 → "Green Masters"
   - Team 4 → "Yellow Legends"
5. Save changes
6. Team names will update throughout the site instantly

### Verification Steps

After running the fix, verify these work:

1. **Homepage loads**: `https://your-site.com/`
2. **Admin panel**: `https://your-site.com/admin/`
3. **Leaderboard**: `https://your-site.com/leaderboard/`
4. **Team names**: Should show updated names from admin
5. **Chart colors**: Should display distinct colors for each team

### Prevention for Future Deployments

Add this to your deployment process:

1. **Build Command** (in Render):
   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```

2. **Start Command** (in Render):
   ```bash
   gunicorn onam_project.wsgi:application
   ```

3. **Always run migrations** before deploying new code

### Troubleshooting

If the fix doesn't work:

1. **Check environment variables** in your hosting platform
2. **Verify database connection** settings
3. **Check build logs** for error messages
4. **Try running migrations individually**:
   ```bash
   python manage.py showmigrations
   python manage.py migrate --fake-initial
   ```

### Team Admin Features

Once fixed, the admin panel provides:

- **Edit team names** - Change display names for all teams
- **Activate/deactivate teams** - Control which teams are active
- **View team statistics** - See player counts and activity
- **Manage events** - Create and score team/individual events
- **Upload questions** - Add new treasure hunt questions

### Contact Support

If you continue having issues:
1. Check the error logs in your hosting platform
2. Verify all environment variables are set correctly
3. Ensure the database is accessible
4. Run the emergency script multiple times if needed

---

**Status**: 🔧 Emergency fix ready for deployment
**Priority**: 🚨 Critical - Site currently down
**Impact**: ✅ Will restore full site functionality including team management
