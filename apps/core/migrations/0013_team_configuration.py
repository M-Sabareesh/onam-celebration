# Generated migration for TeamConfiguration model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_team_event_participation'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_code', models.CharField(help_text="Internal team code (don't change)", max_length=20, unique=True)),
                ('team_name', models.CharField(help_text='Display name for the team', max_length=100)),
                ('is_active', models.BooleanField(default=True, help_text='Whether this team is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Team Configuration',
                'verbose_name_plural': 'Team Configurations',
                'ordering': ['team_code'],
            },
        ),
    ]
