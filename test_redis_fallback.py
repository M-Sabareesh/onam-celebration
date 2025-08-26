#!/usr/bin/env python
"""
Test script to verify Redis fallback is working properly.
"""

import os
import django

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onam_project.settings.production")

# Setup Django
django.setup()

from django.conf import settings
from django.core.cache import cache

def test_cache_and_sessions():
    """Test cache and session configuration."""
    print("🔍 Testing cache and session configuration...")
    
    # Test cache backend
    cache_backend = settings.CACHES['default']['BACKEND']
    print(f"Cache Backend: {cache_backend}")
    
    # Test session engine
    session_engine = settings.SESSION_ENGINE
    print(f"Session Engine: {session_engine}")
    
    # Test cache functionality
    try:
        cache.set('test_key', 'test_value', 30)
        value = cache.get('test_key')
        if value == 'test_value':
            print("✓ Cache is working properly")
        else:
            print("⚠ Cache test failed")
    except Exception as e:
        print(f"⚠ Cache error: {e}")
    
    # Show configuration summary
    if 'redis' in cache_backend.lower():
        print("📡 Using Redis for cache and sessions")
    else:
        print("🗄️ Using database for cache and sessions")

if __name__ == "__main__":
    test_cache_and_sessions()
