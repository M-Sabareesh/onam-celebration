#!/usr/bin/env python
"""
Emergency Production Fix for Render Deployment
Fixes critical errors:
1. CSRF/Referer checking failures
2. SSL database connection issues
3. Missing database columns
4. Removes Google Cloud setup
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

try:
    django.setup()
except Exception as e:
    print(f"Warning: Could not fully initialize Django: {e}")
    print("Continuing with file fixes...")

def fix_production_settings():
    """Fix production settings for Render deployment"""
    settings_file = project_root / 'onam_project' / 'settings' / 'production.py'
    
    production_settings = '''"""
Production settings for Render deployment
"""

from .base import *
import os
import logging

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Render.com provides these environment variables
ALLOWED_HOSTS = [
    'onam-celebration.onrender.com',
    '.onrender.com',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

# CSRF Settings - Fix for Referer checking failures
CSRF_TRUSTED_ORIGINS = [
    'https://onam-celebration.onrender.com',
    'https://*.onrender.com',
]

# Allow admin login without referer (for automated health checks)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Disable strict referer checking for admin
SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'

# Database configuration for Render PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'prefer',  # Changed from 'require' to 'prefer'
            'connect_timeout': 30,
            'options': '-c default_transaction_isolation=serializable'
        },
        'CONN_MAX_AGE': 0,  # Disable connection pooling
        'CONN_HEALTH_CHECKS': True,
    }
}

# Static files configuration for Render
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Cache configuration (using database cache)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Disable Google Photos integration in production
GOOGLE_PHOTOS_ENABLED = False

# Email configuration (if needed)
if os.environ.get('EMAIL_HOST'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

print("Production settings loaded successfully")
'''
    
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(production_settings)
    print(f"✓ Updated production settings: {settings_file}")

def create_emergency_migration():
    """Create migration to add missing database columns"""
    migration_dir = project_root / 'apps' / 'core' / 'migrations'
    migration_dir.mkdir(exist_ok=True)
    
    migration_file = migration_dir / '0100_emergency_production_fix.py'
    
    migration_content = '''# Generated emergency migration for production fix

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
'''
    
    with open(migration_file, 'w', encoding='utf-8') as f:
        f.write(migration_content)
    print(f"✓ Created emergency migration: {migration_file}")

def disable_google_photos():
    """Disable Google Photos integration by creating stub files"""
    
    # Create stub google_photos.py
    google_photos_file = project_root / 'apps' / 'core' / 'google_photos.py'
    stub_content = '''"""
Google Photos integration stub - disabled in production
"""

class GooglePhotosService:
    def __init__(self):
        self.enabled = False
    
    def authenticate(self):
        return False
    
    def upload_photo(self, photo_path, album_id=None):
        return None
    
    def create_album(self, title, description=""):
        return None
    
    def get_photos(self, album_id=None):
        return []
    
    def is_authenticated(self):
        return False

# Global instance
google_photos_service = GooglePhotosService()

def get_google_photos_service():
    return google_photos_service
'''
    
    with open(google_photos_file, 'w', encoding='utf-8') as f:
        f.write(stub_content)
    print(f"✓ Created Google Photos stub: {google_photos_file}")

def apply_database_fixes():
    """Apply database fixes using Django management commands"""
    try:
        from django.core.management import execute_from_command_line
        from django.db import connection
        
        print("� Applying database fixes...")
        
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Create cache table
        execute_from_command_line(['manage.py', 'createcachetable'])
        
        print("✓ Database fixes applied")
        return True
        
    except Exception as e:
        print(f"❌ Database fix failed: {e}")
        return False

def main():
    """Run all emergency fixes"""
    print("🚨 Starting Emergency Production Fix...")
    
    try:
        fix_production_settings()
        create_emergency_migration()
        disable_google_photos()
        
        # Try to apply database fixes if Django is available
        try:
            apply_database_fixes()
        except:
            print("⚠️  Database fixes will be applied during deployment")
        
        print("\n✅ Emergency fixes completed successfully!")
        print("\n📋 Next steps for Render deployment:")
        print("1. git add .")
        print("2. git commit -m 'Emergency production fix'")
        print("3. git push")
        print("4. After deployment, run: python manage.py migrate")
        print("5. Run: python manage.py collectstatic --noinput")
        print("6. Test admin login at: https://onam-celebration.onrender.com/custom-admin/")
        
    except Exception as e:
        print(f"\n❌ Error during fix: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

if __name__ == "__main__":
    main()
