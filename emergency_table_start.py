#!/usr/bin/env python3
"""
EMERGENCY TABLE CREATION AND START
Creates missing tables and starts the server
"""

import os
import sys

def main():
    """Emergency table creation and server start"""
    print("🚨 EMERGENCY: Creating missing tables...")
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')
    
    import django
    django.setup()
    
    from django.db import connection
    
    try:
        with connection.cursor() as cursor:
            # Create main table
            print("📋 Creating core_simpleeventscore...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_simpleeventscore (
                    id BIGSERIAL PRIMARY KEY,
                    team VARCHAR(20) NOT NULL,
                    event_type VARCHAR(20) NOT NULL DEFAULT 'team',
                    points DECIMAL(6,2) NOT NULL DEFAULT 0,
                    notes TEXT NOT NULL DEFAULT '',
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    event_id BIGINT NOT NULL REFERENCES core_event(id) ON DELETE CASCADE
                )
            """)
            
            # Create relationship table
            print("📋 Creating core_simpleeventscore_participants...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_simpleeventscore_participants (
                    id BIGSERIAL PRIMARY KEY,
                    simpleeventscore_id BIGINT NOT NULL REFERENCES core_simpleeventscore(id) ON DELETE CASCADE,
                    player_id BIGINT NOT NULL REFERENCES core_player(id) ON DELETE CASCADE,
                    UNIQUE(simpleeventscore_id, player_id)
                )
            """)
            
            # Add indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS core_simpleeventscore_event_id ON core_simpleeventscore(event_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS core_simpleeventscore_participants_score ON core_simpleeventscore_participants(simpleeventscore_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS core_simpleeventscore_participants_player ON core_simpleeventscore_participants(player_id)")
            
            # Mark migration as applied
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied)
                VALUES ('core', '0015_simple_event_scoring', NOW())
                ON CONFLICT (app, name) DO NOTHING
            """)
            
            print("✅ Emergency tables created successfully!")
            
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        # Continue anyway - server might still work with other features
    
    print("🚀 Starting Gunicorn...")
    
    # Start the server
    port = os.environ.get('PORT', '10000')
    workers = os.environ.get('WEB_CONCURRENCY', '1')
    
    os.execvp('gunicorn', [
        'gunicorn',
        'onam_project.wsgi:application',
        '--bind', f'0.0.0.0:{port}',
        '--workers', str(workers),
        '--timeout', '120',
        '--max-requests', '1000'
    ])

if __name__ == "__main__":
    main()
