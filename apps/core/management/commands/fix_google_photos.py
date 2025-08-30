"""
Django management command to fix Google Photos database issues
and apply the migration for Google Photos fields.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Fix Google Photos database migration issue'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix-db',
            action='store_true',
            help='Fix the database migration issue',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔧 Fixing Google Photos database issue...')
        )

        if options['fix_db'] or True:  # Always run by default
            self.fix_database()

    def fix_database(self):
        """Fix the database migration issue"""
        self.stdout.write('📊 Checking database schema...')
        
        # Check if the columns exist
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='core_playeranswer' 
                AND column_name IN ('google_photos_media_id', 'google_photos_url', 'google_photos_product_url')
            """)
            existing_columns = [row[0] for row in cursor.fetchall()]
        
        if len(existing_columns) == 3:
            self.stdout.write(
                self.style.SUCCESS('✅ Google Photos columns already exist!')
            )
            return
        
        self.stdout.write(f'📍 Found {len(existing_columns)} out of 3 Google Photos columns')
        
        # Apply the migration manually if needed
        try:
            self.stdout.write('🔄 Adding missing Google Photos columns...')
            
            with connection.cursor() as cursor:
                # Add columns one by one if they don't exist
                if 'google_photos_media_id' not in existing_columns:
                    cursor.execute("""
                        ALTER TABLE core_playeranswer 
                        ADD COLUMN google_photos_media_id VARCHAR(200) NULL
                    """)
                    self.stdout.write('✅ Added google_photos_media_id column')
                
                if 'google_photos_url' not in existing_columns:
                    cursor.execute("""
                        ALTER TABLE core_playeranswer 
                        ADD COLUMN google_photos_url TEXT NULL
                    """)
                    self.stdout.write('✅ Added google_photos_url column')
                
                if 'google_photos_product_url' not in existing_columns:
                    cursor.execute("""
                        ALTER TABLE core_playeranswer 
                        ADD COLUMN google_photos_product_url TEXT NULL
                    """)
                    self.stdout.write('✅ Added google_photos_product_url column')
            
            self.stdout.write(
                self.style.SUCCESS('🎉 Database schema updated successfully!')
            )
            
            # Now try to apply migrations to mark them as applied
            try:
                call_command('migrate', '--fake-initial', verbosity=1)
                self.stdout.write(
                    self.style.SUCCESS('✅ Migrations marked as applied!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Could not mark migrations as applied: {e}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to update database schema: {e}')
            )
            
            # Fallback: try normal migration
            try:
                self.stdout.write('🔄 Trying normal migration...')
                call_command('migrate', verbosity=1)
                self.stdout.write(
                    self.style.SUCCESS('✅ Normal migration successful!')
                )
            except Exception as e2:
                self.stdout.write(
                    self.style.ERROR(f'❌ Normal migration also failed: {e2}')
                )
                self.stdout.write('💡 Manual intervention may be required.')

        # Show Google Photos setup information
        self.show_google_photos_info()

    def show_google_photos_info(self):
        """Show Google Photos setup information"""
        self.stdout.write('\n🔑 Google Photos Integration Setup:')
        
        album_url = 'https://photos.app.goo.gl/sDnZoj5VnkZ4yByS6'
        album_id = album_url.split('/')[-1]  # Extract ID from URL
        
        self.stdout.write(f'📸 Album URL: {album_url}')
        self.stdout.write(f'🆔 Album ID: {album_id}')
        
        self.stdout.write('\n📋 To enable Google Photos integration:')
        self.stdout.write('1. Set environment variables in your deployment:')
        self.stdout.write(f'   GOOGLE_PHOTOS_ENABLED=True')
        self.stdout.write(f'   GOOGLE_PHOTOS_ALBUM_ID={album_id}')
        self.stdout.write('2. Set up Google Cloud credentials (optional for now)')
        self.stdout.write('\n💡 For now, photos will be stored locally and can be manually')
        self.stdout.write('   uploaded to the Google Photos album when needed.')
        self.stdout.write('\n🎉 The treasure hunt should work properly now!')
