# Generated migration for Google Photos integration
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playeranswer',
            name='google_photos_media_id',
            field=models.CharField(blank=True, help_text='Google Photos media item ID', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='playeranswer',
            name='google_photos_url',
            field=models.URLField(blank=True, help_text='Direct Google Photos URL', null=True),
        ),
        migrations.AddField(
            model_name='playeranswer',
            name='google_photos_product_url',
            field=models.URLField(blank=True, help_text='Google Photos product page URL', null=True),
        ),
    ]
