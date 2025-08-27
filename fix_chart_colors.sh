#!/bin/bash

# Chart Color Fix Script
echo "🎨 Fixing Chart Colors Issue"
echo "=================================="

# 1. Check if static files directory exists
if [ -d "static/js" ]; then
    echo "✅ Static JS directory exists"
else
    echo "❌ Creating static JS directory"
    mkdir -p static/js
fi

# 2. Collect static files (if in production)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# 3. Check chart.js file
if [ -f "static/js/leaderboard_chart.js" ]; then
    echo "✅ Chart JavaScript file exists"
else
    echo "❌ Chart JavaScript file missing"
fi

# 4. Test the leaderboard view
echo "🧪 Testing leaderboard view..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
django.setup()

from apps.core.views import LeaderboardView
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/leaderboard/')

view = LeaderboardView()
view.request = request

try:
    context = view.get_context_data()
    chart_data = context.get('chart_data', {})
    print('Chart data keys:', list(chart_data.keys()))
    if 'datasets' in chart_data:
        print('Datasets found: ✅')
    else:
        print('Datasets missing: ❌')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "💡 To fix chart colors:"
echo "1. Check browser console for JavaScript errors"
echo "2. Verify Chart.js CDN loads correctly"
echo "3. Ensure static files are served properly"
echo "4. Check template rendering of chart_data"

echo ""
echo "🔧 Manual verification steps:"
echo "1. Open browser dev tools on leaderboard page"
echo "2. Look for console log messages from chart initialization"
echo "3. Check Network tab for 404 errors on static files"
echo "4. Verify chart_data contains color properties"
