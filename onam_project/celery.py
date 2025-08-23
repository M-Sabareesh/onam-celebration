"""
Celery configuration for onam_project.
"""
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onam_project.settings.production')

app = Celery('onam_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    'cleanup-expired-verification-codes': {
        'task': 'apps.accounts.tasks.cleanup_expired_verification_codes',
        'schedule': 300.0,  # Run every 5 minutes
    },
    'send-game-reminders': {
        'task': 'apps.games.tasks.send_game_reminders',
        'schedule': 3600.0,  # Run every hour
    },
}

app.conf.timezone = 'Europe/Stockholm'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
