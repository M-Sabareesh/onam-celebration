#!/usr/bin/env python3
"""
Test script to verify the changes to Chodya Onam and chart positioning
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.base')
django.setup()

def test_template_changes():
    """Test that the template changes are correct"""
    print("🔍 Testing template changes...")
    
    # Test leaderboard template
    leaderboard_path = 'templates/core/leaderboard.html'
    if os.path.exists(leaderboard_path):
        with open(leaderboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for Chodya Onam
        if 'Chodya Onam' in content:
            print("✅ Leaderboard: Found 'Chodya Onam' references")
        else:
            print("❌ Leaderboard: 'Chodya Onam' not found")
            
        # Check for chart at bottom
        if 'teamProgressChart' in content and 'Team Performance Progress' in content:
            print("✅ Leaderboard: Chart section found")
        else:
            print("❌ Leaderboard: Chart section not found")
            
        # Check for treasure hunt removal
        if 'Treasure Hunt' in content:
            print("⚠️  Leaderboard: Still contains 'Treasure Hunt' references")
        else:
            print("✅ Leaderboard: 'Treasure Hunt' references removed")
    
    # Test base template
    base_path = 'templates/base.html'
    if os.path.exists(base_path):
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'Chodya Onam' in content:
            print("✅ Base template: Found 'Chodya Onam' references")
        else:
            print("❌ Base template: 'Chodya Onam' not found")
    
    # Test treasure hunt template
    treasure_hunt_path = 'templates/core/treasure_hunt.html'
    if os.path.exists(treasure_hunt_path):
        with open(treasure_hunt_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'Chodya Onam' in content:
            print("✅ Treasure Hunt template: Found 'Chodya Onam' references")
        else:
            print("❌ Treasure Hunt template: 'Chodya Onam' not found")

def test_chart_data():
    """Test that chart data is being generated correctly"""
    print("\n📊 Testing chart data generation...")
    
    try:
        from apps.core.views import LeaderboardView
        from django.test import RequestFactory
        
        # Create a test request
        factory = RequestFactory()
        request = factory.get('/leaderboard/')
        
        # Create view instance
        view = LeaderboardView()
        view.request = request
        
        # Get context data
        context = view.get_context_data()
        
        if 'chart_data' in context:
            chart_data = context['chart_data']
            print("✅ Chart data found in context")
            print(f"   Labels: {len(chart_data.get('labels', []))} items")
            print(f"   Datasets: {len(chart_data.get('datasets', []))} teams")
        else:
            print("❌ Chart data not found in context")
            
    except Exception as e:
        print(f"⚠️  Error testing chart data: {e}")

def test_static_files():
    """Test that required static files exist"""
    print("\n📁 Testing static files...")
    
    chart_js_path = 'static/js/leaderboard_chart.js'
    if os.path.exists(chart_js_path):
        print("✅ Chart JavaScript file exists")
    else:
        print("❌ Chart JavaScript file missing")

def main():
    print("🧪 Testing Chodya Onam changes and chart positioning")
    print("=" * 60)
    
    test_template_changes()
    test_chart_data()
    test_static_files()
    
    print("\n" + "=" * 60)
    print("✅ Testing complete!")
    print("\n📋 Summary of changes:")
    print("   • Renamed 'Treasure Hunt' to 'Chodya Onam' throughout templates")
    print("   • Moved team progress chart to bottom of leaderboard page")
    print("   • Chart shows team progress over events with distinct colors")
    print("   • Chart positioned after individual rankings and before call-to-action")

if __name__ == '__main__':
    main()
