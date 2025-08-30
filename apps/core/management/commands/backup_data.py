"""
Django management command to backup data to GitHub
"""
import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core import serializers
from apps.core.models import Player, TreasureHuntQuestion, PlayerAnswer, Event, EventParticipation, EventVote, EventScore


class Command(BaseCommand):
    help = 'Backup application data to JSON files for GitHub storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='data_backup',
            help='Directory to save backup files'
        )
        parser.add_argument(
            '--include-players',
            action='store_true',
            help='Include player data in backup'
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']
        include_players = options['include_players']
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        self.stdout.write(self.style.SUCCESS(f'Starting data backup to {output_dir}/'))
        
        # Backup questions (always include)
        self.backup_model(TreasureHuntQuestion, f'{output_dir}/questions.json')
        
        # Backup events (always include)
        self.backup_model(Event, f'{output_dir}/events.json')
        
        if include_players:
            # Backup player data (optional, as this changes frequently)
            self.backup_model(Player, f'{output_dir}/players_{timestamp}.json')
            self.backup_model(PlayerAnswer, f'{output_dir}/player_answers_{timestamp}.json')
            self.backup_model(EventParticipation, f'{output_dir}/event_participations_{timestamp}.json')
            self.backup_model(EventVote, f'{output_dir}/event_votes_{timestamp}.json')
            self.backup_model(EventScore, f'{output_dir}/event_scores_{timestamp}.json')
        
        # Create a backup info file
        backup_info = {
            'timestamp': datetime.now().isoformat(),
            'django_version': self.get_django_version(),
            'backup_type': 'full' if include_players else 'structure_only',
            'files_created': self.get_backup_files(output_dir)
        }
        
        with open(f'{output_dir}/backup_info.json', 'w') as f:
            json.dump(backup_info, f, indent=2)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Backup completed successfully!')
        )
        
        # Instructions for GitHub
        self.stdout.write('\n' + '='*50)
        self.stdout.write('GITHUB SETUP INSTRUCTIONS:')
        self.stdout.write('='*50)
        self.stdout.write('1. Create a new repository on GitHub (e.g., onam-celebration-data)')
        self.stdout.write(f'2. Upload the {output_dir}/ folder to your repository')
        self.stdout.write('3. Get the raw file URLs for the JSON files')
        self.stdout.write('4. Add these URLs to your environment variables:')
        self.stdout.write('   - GITHUB_BACKUP_BASE_URL=https://raw.githubusercontent.com/yourusername/onam-celebration-data/main/data_backup/')
        self.stdout.write('5. Use the restore_data command on Render startup')

    def backup_model(self, model_class, output_file):
        """Backup a single model to JSON file"""
        try:
            queryset = model_class.objects.all()
            count = queryset.count()
            
            if count > 0:
                with open(output_file, 'w') as f:
                    serializers.serialize('json', queryset, indent=2, stream=f)
                self.stdout.write(f'✅ Backed up {count} {model_class.__name__} records to {output_file}')
            else:
                self.stdout.write(f'ℹ️  No {model_class.__name__} records to backup')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error backing up {model_class.__name__}: {e}')
            )

    def get_django_version(self):
        """Get Django version"""
        try:
            import django
            return django.get_version()
        except:
            return 'unknown'

    def get_backup_files(self, output_dir):
        """Get list of created backup files"""
        try:
            return [f for f in os.listdir(output_dir) if f.endswith('.json')]
        except:
            return []
