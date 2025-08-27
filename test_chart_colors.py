#!/usr/bin/env python3
"""
Simple test to create sample chart data with hardcoded colors
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
django.setup()

def create_color_test_data():
    """Create test data with explicit colors"""
    try:
        from apps.core.views import LeaderboardView
        from django.test import RequestFactory
        
        # Create a test request
        factory = RequestFactory()
        request = factory.get('/leaderboard/')
        
        # Create view instance
        view = LeaderboardView()
        view.request = request
        
        # Mock team data with simple structure
        test_team_data = {
            'malapuram': {
                'name': 'Malapuram',
                'treasure_hunt_score': 45,
                'event_scores': {'Dance': 20, 'Singing': 15},
                'total_score': 80,
                'players': []
            },
            'pathanamthitta': {
                'name': 'Pathanamthitta', 
                'treasure_hunt_score': 35,
                'event_scores': {'Dance': 25, 'Singing': 10},
                'total_score': 70,
                'players': []
            },
            'ernakulam': {
                'name': 'Ernakulam',
                'treasure_hunt_score': 40,
                'event_scores': {'Dance': 15, 'Singing': 20},
                'total_score': 75,
                'players': []
            },
            'thiruvananthapuram': {
                'name': 'Thiruvananthapuram',
                'treasure_hunt_score': 30,
                'event_scores': {'Dance': 18, 'Singing': 12},
                'total_score': 60,
                'players': []
            }
        }
        
        # Generate chart data
        chart_data = view.get_team_progress_data(test_team_data)
        
        print("🎨 Generated Chart Data:")
        print(f"Labels: {chart_data['labels']}")
        print(f"Datasets: {chart_data['datasets']}")
        
        # Create a test HTML file to verify colors
        test_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Chart Color Test</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Team Progress Chart Color Test</h1>
    <div style="width: 800px; height: 400px;">
        <canvas id="testChart"></canvas>
    </div>
    
    <script>
    const chartData = {{
        labels: {chart_data['labels']},
        datasets: {chart_data['datasets']}
    }};
    
    console.log('Test Chart Data:', chartData);
    
    const ctx = document.getElementById('testChart').getContext('2d');
    new Chart(ctx, {{
        type: 'line',
        data: chartData,
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{ position: 'top' }},
                title: {{
                    display: true,
                    text: 'Team Progress Test'
                }}
            }},
            scales: {{
                y: {{ beginAtZero: true }}
            }}
        }}
    }});
    </script>
</body>
</html>
        """
        
        with open('chart_color_test.html', 'w') as f:
            f.write(test_html)
            
        print("\n✅ Created chart_color_test.html")
        print("   Open this file in your browser to test colors")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 Creating Chart Color Test")
    print("=" * 40)
    
    if create_color_test_data():
        print("\n🎯 Instructions:")
        print("   1. Open chart_color_test.html in your browser")
        print("   2. Check browser console for data logs")
        print("   3. Verify each team has different colors")
        print("   4. If colors work here but not in main site,")
        print("      the issue is in template data passing")
    else:
        print("\n❌ Test creation failed")

if __name__ == '__main__':
    main()
