#!/bin/bash
# IMMEDIATE EMERGENCY FIX for Render
# Creates missing table and starts server

echo "🚨 EMERGENCY FIX: Creating missing core_simpleeventscore table"

# Force create the missing table using raw SQL
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
django.setup()
from django.db import connection

sql = '''
CREATE TABLE IF NOT EXISTS core_simpleeventscore (
    id BIGSERIAL PRIMARY KEY,
    team VARCHAR(20) NOT NULL,
    event_type VARCHAR(20) DEFAULT 'team' NOT NULL,
    points DECIMAL(6,2) DEFAULT 0 NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    event_id BIGINT NOT NULL REFERENCES core_event(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS core_simpleeventscore_participants (
    id BIGSERIAL PRIMARY KEY,
    simpleeventscore_id BIGINT NOT NULL REFERENCES core_simpleeventscore(id) ON DELETE CASCADE,
    player_id BIGINT NOT NULL REFERENCES core_player(id) ON DELETE CASCADE,
    UNIQUE(simpleeventscore_id, player_id)
);

INSERT INTO django_migrations (app, name, applied) 
VALUES ('core', '0015_simple_event_scoring', NOW())
ON CONFLICT (app, name) DO NOTHING;
'''

try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
    print('✅ Table created successfully')
except Exception as e:
    print(f'⚠️ Table creation: {e}')
"

echo "🔧 Running migrations..."
python manage.py migrate --noinput || echo "Migration issues but continuing"

echo "🔧 Collecting static files..."
python manage.py collectstatic --noinput || echo "Static collection issues but continuing"

echo "📁 Creating media directories..."
mkdir -p media/question_images media/treasure_hunt_photos media/avatars

echo "🌐 Starting server..."
exec gunicorn onam_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
