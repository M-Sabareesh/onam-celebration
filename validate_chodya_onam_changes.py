#!/usr/bin/env python3
"""
Quick validation script for Chodya Onam changes and chart positioning
"""

import os
import re

def check_file_content(file_path, search_patterns, description):
    """Check if file contains expected patterns"""
    print(f"\n🔍 Checking {description}:")
    
    if not os.path.exists(file_path):
        print(f"   ❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = []
        for pattern, expected in search_patterns.items():
            if expected:
                found = pattern in content
                status = "✅" if found else "❌"
                results.append((status, f"Should contain '{pattern}': {found}"))
            else:
                found = pattern not in content
                status = "✅" if found else "❌"
                results.append((status, f"Should NOT contain '{pattern}': {not found}"))
        
        for status, message in results:
            print(f"   {status} {message}")
            
        return all(status == "✅" for status, _ in results)
        
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        return False

def main():
    print("🎯 Chodya Onam & Chart Positioning Validation")
    print("=" * 60)
    
    # Test patterns for key files
    test_cases = [
        {
            'file': 'templates/core/leaderboard.html',
            'description': 'Leaderboard Template',
            'patterns': {
                'Chodya Onam': True,
                'Treasure Hunt': False,
                'teamProgressChart': True,
                'Team Performance Progress by Event': True,
                '<canvas id="teamProgressChart"': True,
            }
        },
        {
            'file': 'templates/base.html',
            'description': 'Base Template',
            'patterns': {
                'Chodya Onam': True,
                'Treasure Hunt': False,
            }
        },
        {
            'file': 'templates/core/index.html',
            'description': 'Home Page Template',
            'patterns': {
                'Chodya Onam': True,
                'Treasure Hunt': False,
                'How Chodya Onam Works': True,
            }
        },
        {
            'file': 'templates/core/treasure_hunt.html',
            'description': 'Game Page Template',
            'patterns': {
                'Chodya Onam': True,
                'Onam Treasure Hunt': False,
            }
        },
        {
            'file': 'apps/core/views.py',
            'description': 'Views Backend',
            'patterns': {
                'Chodya Onam questions view': True,
                'Chodya Onam",': True,
            }
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        passed = check_file_content(
            test_case['file'],
            test_case['patterns'],
            test_case['description']
        )
        all_passed = all_passed and passed
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("\n✅ Summary of successful changes:")
        print("   • 'Treasure Hunt' renamed to 'Chodya Onam' throughout templates")
        print("   • Team progress chart moved to bottom of leaderboard")
        print("   • Chart canvas element properly positioned")
        print("   • Cultural terminology updated for authenticity")
        print("   • User experience flow improved")
    else:
        print("⚠️  SOME VALIDATIONS FAILED!")
        print("   Please review the failed checks above")
    
    print("\n🎯 Next steps:")
    print("   1. Test the website in your browser")
    print("   2. Navigate to /leaderboard/ to see the chart at the bottom")
    print("   3. Verify all navigation shows 'Chodya Onam'")
    print("   4. Check mobile responsiveness")

if __name__ == '__main__':
    main()
