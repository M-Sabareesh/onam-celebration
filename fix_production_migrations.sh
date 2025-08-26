#!/bin/bash

# Production Migration Fix Script
echo "=== Onam Celebration - Production Migration Fix ==="
echo "This script will apply all missing migrations to fix the leaderboard."
echo ""

# Change to project directory
cd "$(dirname "$0")"

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Make sure you're in the project root."
    exit 1
fi

echo "✓ Found manage.py in current directory"

# Show current migration status
echo ""
echo "=== Current Migration Status ==="
python manage.py showmigrations core

echo ""
echo "=== Applying Missing Migrations ==="

# Apply individual migrations in order
echo ">>> Applying migration 0010 (Individual Event Models)..."
python manage.py migrate core 0010
if [ $? -eq 0 ]; then
    echo "✓ Migration 0010 applied successfully"
else
    echo "⚠ Warning: Migration 0010 failed or already applied"
fi

echo ""
echo ">>> Applying migration 0011 (Fix Individual Vote Null Fields)..."
python manage.py migrate core 0011
if [ $? -eq 0 ]; then
    echo "✓ Migration 0011 applied successfully"
else
    echo "⚠ Warning: Migration 0011 failed or already applied"
fi

echo ""
echo ">>> Applying migration 0012 (Team Event Participation)..."
python manage.py migrate core 0012
if [ $? -eq 0 ]; then
    echo "✓ Migration 0012 applied successfully"
else
    echo "⚠ Warning: Migration 0012 failed or already applied"
fi

echo ""
echo ">>> Applying any remaining migrations..."
python manage.py migrate
if [ $? -eq 0 ]; then
    echo "✓ All migrations applied successfully"
else
    echo "⚠ Warning: Some migrations may have failed"
fi

# Show final status
echo ""
echo "=== Final Migration Status ==="
python manage.py showmigrations core

echo ""
echo "=== Testing Database Tables ==="

# Test if we can access the new models
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
django.setup()

from apps.core.models import IndividualEventScore, TeamEventParticipation, IndividualParticipation, IndividualEventVote

try:
    count1 = IndividualEventScore.objects.count()
    count2 = TeamEventParticipation.objects.count()
    count3 = IndividualParticipation.objects.count()
    count4 = IndividualEventVote.objects.count()
    
    print('✅ Database Test Results:')
    print(f'   IndividualEventScore records: {count1}')
    print(f'   TeamEventParticipation records: {count2}')
    print(f'   IndividualParticipation records: {count3}')
    print(f'   IndividualEventVote records: {count4}')
    print('')
    print('🎉 All models are accessible! The leaderboard should now work.')
except Exception as e:
    print(f'❌ Database test failed: {e}')
    print('The migrations may not have been applied correctly.')
"

echo ""
echo "=== Migration Fix Complete ==="
echo "If all tests passed, you can now:"
echo "1. Restart your Django development server"
echo "2. Visit the leaderboard page"
echo "3. The Malayalam branding and Maveli images should be visible"
echo "4. Individual and team scoring should work properly"
echo ""
echo "If there are still errors, check the Django logs for details."
