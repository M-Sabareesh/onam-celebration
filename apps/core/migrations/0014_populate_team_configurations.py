# Data migration to populate initial team configurations

from django.db import migrations


def create_initial_teams(apps, schema_editor):
    TeamConfiguration = apps.get_model('core', 'TeamConfiguration')
    
    # Create initial team configurations
    default_teams = [
        ('team_1', 'Team 1'),
        ('team_2', 'Team 2'),
        ('team_3', 'Team 3'),
        ('team_4', 'Team 4'),
        ('unassigned', 'Unassigned'),
    ]
    
    for team_code, team_name in default_teams:
        TeamConfiguration.objects.get_or_create(
            team_code=team_code,
            defaults={'team_name': team_name, 'is_active': True}
        )


def reverse_create_initial_teams(apps, schema_editor):
    TeamConfiguration = apps.get_model('core', 'TeamConfiguration')
    TeamConfiguration.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_team_configuration'),
    ]

    operations = [
        migrations.RunPython(create_initial_teams, reverse_create_initial_teams),
    ]
