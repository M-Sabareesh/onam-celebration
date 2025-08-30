"""
Django management command to restore data from GitHub
"""
import os
import json
import requests
from django.core.management.base import BaseCommand
from django.core import serializers
from django.db import transaction
from apps.core.models import Player, TreasureHuntQuestion, PlayerAnswer, Event, EventParticipation, EventVote, EventScore


class Command(BaseCommand):
    help = 'Restore application data from GitHub backup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--github-base-url',
            type=str,
            help='Base URL for GitHub raw files (e.g., https://raw.githubusercontent.com/user/repo/main/data_backup/)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force restore even if data exists'
        )
        parser.add_argument(
            '--structure-only',
            action='store_true',
            help='Only restore questions and events, not player data'
        )

    def handle(self, *args, **options):
        github_base_url = options.get('github_base_url') or os.environ.get('GITHUB_BACKUP_BASE_URL')
        force = options['force']
        structure_only = options['structure_only']
        
        if not github_base_url:
            self.stdout.write(
                self.style.ERROR('❌ GitHub base URL not provided. Set GITHUB_BACKUP_BASE_URL environment variable or use --github-base-url')
            )
            return
        
        if not github_base_url.endswith('/'):
            github_base_url += '/'
        
        self.stdout.write(self.style.SUCCESS(f'Starting data restore from {github_base_url}'))
        
        # Check if data already exists
        if not force and not structure_only:
            if Player.objects.exists() or TreasureHuntQuestion.objects.exists():
                self.stdout.write(
                    self.style.WARNING('⚠️  Data already exists. Use --force to overwrite or --structure-only to restore only questions/events')
                )
                return
        
        try:
            with transaction.atomic():
                # Always restore questions and events (structure)
                self.restore_questions(github_base_url, force)
                self.restore_events(github_base_url, force)
                
                if not structure_only:
                    # Restore player data if requested
                    self.restore_player_data(github_base_url, force)
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Data restore completed successfully!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error during restore: {e}')
            )
            raise

    def restore_questions(self, base_url, force=False):
        """Restore treasure hunt questions"""
        if not force and TreasureHuntQuestion.objects.exists():
            self.stdout.write('ℹ️  Questions already exist, skipping...')
            return
        
        url = f'{base_url}questions.json'
        data = self.download_json(url)
        
        if data:
            if force:
                TreasureHuntQuestion.objects.all().delete()
            
            count = 0
            for obj_data in serializers.deserialize('json', json.dumps(data)):
                obj_data.save()
                count += 1
            
            self.stdout.write(f'✅ Restored {count} treasure hunt questions')
        else:
            self.stdout.write('ℹ️  No questions data found')

    def restore_events(self, base_url, force=False):
        """Restore events"""
        if not force and Event.objects.exists():
            self.stdout.write('ℹ️  Events already exist, skipping...')
            return
        
        url = f'{base_url}events.json'
        data = self.download_json(url)
        
        if data:
            if force:
                Event.objects.all().delete()
            
            count = 0
            for obj_data in serializers.deserialize('json', json.dumps(data)):
                obj_data.save()
                count += 1
            
            self.stdout.write(f'✅ Restored {count} events')
        else:
            self.stdout.write('ℹ️  No events data found')

    def restore_player_data(self, base_url, force=False):
        """Restore player data (optional)"""
        # Note: For production, you might want to restore only the structure
        # and let users re-register, as player data changes frequently
        self.stdout.write('ℹ️  Player data restore not implemented - users will re-register')

    def download_json(self, url):
        """Download JSON data from URL"""
        try:
            self.stdout.write(f'📥 Downloading: {url}')
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(f'⚠️  Could not download {url}: {e}')
            return None
        except json.JSONDecodeError as e:
            self.stdout.write(f'⚠️  Invalid JSON from {url}: {e}')
            return None

    def restore_model_from_url(self, model_class, url, force=False):
        """Generic method to restore a model from URL"""
        if not force and model_class.objects.exists():
            self.stdout.write(f'ℹ️  {model_class.__name__} already exists, skipping...')
            return
        
        data = self.download_json(url)
        if data:
            if force:
                model_class.objects.all().delete()
            
            count = 0
            for obj_data in serializers.deserialize('json', json.dumps(data)):
                obj_data.save()
                count += 1
            
            self.stdout.write(f'✅ Restored {count} {model_class.__name__} records')
        else:
            self.stdout.write(f'ℹ️  No {model_class.__name__} data found')
