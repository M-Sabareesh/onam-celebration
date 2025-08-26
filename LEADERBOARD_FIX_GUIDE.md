# 🚨 Leaderboard Database Fix - Production Issue

## Problem
The leaderboard is failing with this error:
```
psycopg.errors.UndefinedTable: relation "core_individualeventscore" does not exist
```

This means the database migrations for individual event models haven't been applied to production.

## ✅ Quick Fixes Applied

### 1. Fixed Views (Immediate)
I've updated `apps/core/views.py` to handle missing tables gracefully:
- Added try/catch blocks around IndividualEventScore queries
- Leaderboard will now work even without the tables
- No more 500 errors when accessing /leaderboard/

### 2. Emergency Migration Script
Created `emergency_leaderboard_fix.py` to apply missing migrations.

## 🚀 Solutions (Choose One)

### Option 1: Apply Migrations (Recommended)
Run this on your Render server:
```bash
python manage.py migrate core 0010
python manage.py migrate core 0011
python manage.py migrate core 0012
python manage.py migrate
```

### Option 2: Emergency Script
Run the emergency fix script:
```bash
python emergency_leaderboard_fix.py
```

### Option 3: Update Build Script
Add migrations to your Render build script:
```bash
#!/bin/bash
pip install -r requirements.txt
python manage.py migrate  # This line is crucial
python manage.py collectstatic --noinput
```

## 🔍 What Tables Are Missing

The error indicates these tables need to be created:
- `core_individualeventscore` - Individual player scores
- `core_individualparticipation` - Individual event participation
- `core_individualeventvote` - Individual event voting
- `core_teameventparticipation` - Team event participation tracking

## 📊 Current Status

### ✅ Working Now:
- **Homepage** - Shows Maveli images
- **Admin** - Custom admin interface  
- **Treasure Hunt** - Game functionality
- **Player Registration** - Working normally
- **Leaderboard** - Basic functionality (with missing table handling)

### 🔧 Will Work After Migration:
- **Full Leaderboard** - Complete individual and team scoring
- **Individual Event Scoring** - Player-specific achievements
- **Team Participation Tracking** - Checkbox selection system
- **Enhanced Admin** - All event scoring features

## 🎯 Expected Results After Fix

Once migrations are applied:
- ✅ **No more leaderboard errors**
- ✅ **Complete team participation system**
- ✅ **Individual event scoring**
- ✅ **Enhanced admin with participant selection**
- ✅ **Auto-calculation**: participants × points_per_participant

## 🚨 Immediate Action

Your website is mostly working now, but to get full functionality:

1. **Access Render Shell/Console**
2. **Run**: `python manage.py migrate`
3. **Restart the service**

## 📞 Alternative Quick Fix

If you can't access the server directly, the leaderboard will now show:
- Basic team scores (from existing EventScore table)
- Treasure hunt scores 
- Team standings
- Graceful handling of missing individual scores

The system degrades gracefully instead of crashing!

## 🎉 Team Participation Features

Once migrations are applied, you'll have:
- **Checkbox selection** of team members who participated
- **Auto-calculation**: 5 players × 10 points = 50 total points
- **Enhanced admin interface** for event scoring
- **Complete Malayalam-branded experience**

Your website is functional now and will be fully featured once the migrations are applied! 🎊
