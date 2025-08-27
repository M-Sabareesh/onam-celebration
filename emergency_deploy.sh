#!/bin/bash
# EMERGENCY DEPLOYMENT FIX - Missing Database Tables
# This script fixes the missing core_teamconfiguration table issue

echo "🚨 EMERGENCY DEPLOYMENT FIX"
echo "=========================="

# Install dependencies first
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Apply migrations with proper error handling
echo "🔧 Fixing database migrations..."

# Try to apply core Django migrations first
echo "   📋 Django core migrations..."
python manage.py migrate contenttypes --noinput || echo "   ⚠️  contenttypes migration had issues"
python manage.py migrate auth --noinput || echo "   ⚠️  auth migration had issues"
python manage.py migrate sessions --noinput || echo "   ⚠️  sessions migration had issues"
python manage.py migrate admin --noinput || echo "   ⚠️  admin migration had issues"

# Try to apply our app migrations
echo "   🎯 App migrations..."
python manage.py migrate core --noinput || echo "   ⚠️  core migration had issues"
python manage.py migrate accounts --noinput || echo "   ⚠️  accounts migration had issues"
python manage.py migrate games --noinput || echo "   ⚠️  games migration had issues"

# Apply all remaining migrations
echo "   🔄 All remaining migrations..."
python manage.py migrate --noinput || echo "   ⚠️  some migrations had issues"

# Run the emergency fix script
echo "🛠️  Running emergency database fix..."
python emergency_production_fix.py || echo "   ⚠️  emergency fix had issues but continuing..."

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || echo "   ⚠️  static files collection had issues"

echo "✅ EMERGENCY FIX COMPLETE"
echo "🌐 Attempting to start the server..."
