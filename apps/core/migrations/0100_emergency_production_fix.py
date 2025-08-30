# Generated emergency migration for production fix

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0099_emergency_fix'),  # Adjust this to your latest migration
    ]

    operations = [
        # Add missing columns if they don't exist
        migrations.RunSQL(
            """
            DO $$
            BEGIN
                -- Add points_per_participant column if it doesn't exist
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'core_simpleeventscore' 
                    AND column_name = 'points_per_participant'
                ) THEN
                    ALTER TABLE core_simpleeventscore 
                    ADD COLUMN points_per_participant INTEGER DEFAULT 0;
                END IF;
                
                -- Add any other missing columns
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'core_simpleeventscore' 
                    AND column_name = 'max_participants'
                ) THEN
                    ALTER TABLE core_simpleeventscore 
                    ADD COLUMN max_participants INTEGER DEFAULT 1;
                END IF;
                
                -- Create cache table if it doesn't exist
                CREATE TABLE IF NOT EXISTS cache_table (
                    cache_key VARCHAR(255) PRIMARY KEY,
                    value TEXT,
                    expires TIMESTAMP
                );
                
            END $$;
            """,
            reverse_sql="-- No reverse operation"
        ),
    ]
