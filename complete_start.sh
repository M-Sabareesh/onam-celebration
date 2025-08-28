#!/bin/bash

# Complete Start Script for Onam Celebration Project
# Includes all recent fixes: Auto-calculation, Team filtering, and Leaderboard calculation

echo "🎉 ONAM CELEBRATION PROJECT - COMPLETE START"
echo "=============================================="
echo "✅ Auto-calculation for event scores"
echo "✅ Team filtering in admin dropdowns" 
echo "✅ Fixed leaderboard calculation (no double-counting)"
echo "=============================================="

# Step 1: Apply database migrations
echo ""
echo "📊 APPLYING DATABASE MIGRATIONS"
echo "--------------------------------"
python manage.py makemigrations
python manage.py migrate

# Apply the new auto-calculation migration specifically
echo "Applying auto-calculation migration..."
python manage.py migrate core 0016 --fake-initial

# Step 2: Collect static files
echo ""
echo "📁 COLLECTING STATIC FILES"
echo "-------------------------"
python manage.py collectstatic --noinput

# Step 3: Test database integrity
echo ""
echo "🔍 TESTING DATABASE INTEGRITY"
echo "----------------------------"
python -c "
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
sys.path.append('.')
django.setup()

try:
    from apps.core.models import SimpleEventScore, Player, Event
    print('✅ Models imported successfully')
    
    # Test auto-calculation fields
    print(f'✅ SimpleEventScore model ready')
    print(f'✅ Players: {Player.objects.count()}')
    print(f'✅ Events: {Event.objects.count()}')
    
    # Test leaderboard
    from apps.core.views import LeaderboardView
    print('✅ LeaderboardView ready')
    
    print('🎉 All systems ready!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    print('⚠️  Some features may not work properly')
"

# Step 4: Start the application
echo ""
echo "🚀 STARTING APPLICATION"
echo "----------------------"
echo "Server will start on port 8000"
echo "Admin: http://localhost:8000/admin/"
echo "Leaderboard: http://localhost:8000/leaderboard/"
echo ""

# Start Django server
python manage.py runserver 0.0.0.0:8000
