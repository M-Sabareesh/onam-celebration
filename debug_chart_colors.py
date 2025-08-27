#!/usr/bin/env python3
"""
Debug script to check chart color data generation
"""

import os
import sys
import django
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
django.setup()

def debug_chart_colors():
    """Debug the chart color generation"""
    print("🎨 Debugging Chart Color Generation")
    print("=" * 50)
    
    try:
        from apps.core.views import LeaderboardView
        from apps.core.models import Player
        from django.test import RequestFactory
        
        # Create a test request
        factory = RequestFactory()
        request = factory.get('/leaderboard/')
        
        # Create view instance
        view = LeaderboardView()
        view.request = request
        
        # Get context data
        context = view.get_context_data()
        chart_data = context.get('chart_data', {})
        
        print("📊 Chart Data Structure:")
        print(f"   Labels: {chart_data.get('labels', 'None')}")
        
        if 'datasets' in chart_data:
            datasets_str = chart_data['datasets']
            try:
                # Parse the JSON string to see actual data
                datasets = json.loads(datasets_str)
                print(f"\n🎯 Number of datasets (teams): {len(datasets)}")
                
                for i, dataset in enumerate(datasets):
                    print(f"\n   Team {i+1}: {dataset.get('label', 'Unknown')}")
                    print(f"      Border Color: {dataset.get('borderColor', 'None')}")
                    print(f"      Background Color: {dataset.get('backgroundColor', 'None')}")
                    print(f"      Data Points: {len(dataset.get('data', []))}")
                    print(f"      Sample Data: {dataset.get('data', [])[:3]}...")
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ Error parsing datasets JSON: {e}")
                print(f"   Raw datasets: {datasets_str[:200]}...")
        else:
            print("   ❌ No datasets found in chart data")
        
        # Check team data structure
        print(f"\n🏃 Team Choices Available:")
        for code, name in Player.TEAM_CHOICES:
            print(f"   {code}: {name}")
            
        # Test the color mapping directly
        print(f"\n🌈 Testing Color Mapping:")
        team_colors = {
            'malapuram': '#E53E3E',        # Bright Red
            'pathanamthitta': '#3182CE',   # Blue  
            'ernakulam': '#D69E2E',        # Golden Orange
            'thiruvananthapuram': '#38A169', # Green
            'unassigned': '#805AD5'        # Purple
        }
        
        for code, color in team_colors.items():
            print(f"   {code}: {color}")
            
    except Exception as e:
        print(f"❌ Error during debugging: {e}")
        import traceback
        traceback.print_exc()

def check_static_file():
    """Check if the chart JS file exists and has correct content"""
    print(f"\n📁 Checking Static Files:")
    
    chart_js_path = 'static/js/leaderboard_chart.js'
    if os.path.exists(chart_js_path):
        print(f"   ✅ Chart JavaScript file exists")
        with open(chart_js_path, 'r') as f:
            content = f.read()
            if 'borderColor' in content and 'backgroundColor' in content:
                print(f"   ✅ Color properties referenced in JS")
            else:
                print(f"   ⚠️  Color properties might not be used correctly in JS")
    else:
        print(f"   ❌ Chart JavaScript file missing")

def main():
    debug_chart_colors()
    check_static_file()
    
    print(f"\n💡 Debugging Complete!")
    print(f"\nIf colors are still not working, check:")
    print(f"   1. Browser console for JavaScript errors")
    print(f"   2. Network tab to ensure chart.js loads")
    print(f"   3. Static files are being served correctly")
    print(f"   4. Django template is rendering chart_data correctly")

if __name__ == '__main__':
    main()
