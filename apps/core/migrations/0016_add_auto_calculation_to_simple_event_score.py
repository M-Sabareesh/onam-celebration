# Generated manually for auto-calculation fields in SimpleEventScore

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_simple_event_scoring'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpleeventscore',
            name='auto_calculate_points',
            field=models.BooleanField(default=False, help_text='Automatically calculate total points based on participants'),
        ),
        migrations.AddField(
            model_name='simpleeventscore',
            name='points_per_participant',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Points awarded per participating player', max_digits=6),
        ),
    ]
