#!/usr/bin/env python3
"""
Create migration for SimpleEventScore model
"""
import os
import sys
import django

# Add current directory to Python path  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

def main():
    try:
        django.setup()
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'makemigrations', 'core', '--name', 'simple_event_scoring'])
        print("Migration created successfully!")
    except Exception as e:
        print(f"Error creating migration: {e}")
        
        # Try to create the migration manually
        try:
            from django.db import migrations, models
            
            migration_content = '''# Generated migration for SimpleEventScore

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_event_individual_scoring_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleEventScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(choices=[('team_1', 'Team 1'), ('team_2', 'Team 2'), ('team_3', 'Team 3'), ('team_4', 'Team 4'), ('unassigned', 'Unassigned')], help_text='Team to award points to', max_length=20)),
                ('event_type', models.CharField(choices=[('team', 'Team Event'), ('individual', 'Individual Event'), ('hybrid', 'Hybrid (Team with Individual Participants)')], default='team', max_length=20)),
                ('points', models.DecimalField(decimal_places=2, default=0, help_text='Points awarded', max_digits=6)),
                ('notes', models.TextField(blank=True, help_text='Optional notes about the scoring')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='simple_scores', to='core.event')),
                ('participants', models.ManyToManyField(blank=True, help_text='Individual participants (for hybrid events)', to='core.player')),
            ],
            options={
                'verbose_name': 'Simple Event Score',
                'verbose_name_plural': 'Simple Event Scores',
                'ordering': ['-points', 'team'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='simpleeventcore',
            unique_together={('event', 'team')},
        ),
    ]
'''
            
            # Write migration file
            migration_file = 'apps/core/migrations/0015_simple_event_scoring.py'
            with open(migration_file, 'w') as f:
                f.write(migration_content)
            print(f"Manual migration created: {migration_file}")
            
        except Exception as e2:
            print(f"Error creating manual migration: {e2}")

if __name__ == '__main__':
    main()
