from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    
    def ready(self):
        # Temporarily disabled to avoid import errors during initial setup
        # import apps.accounts.signals
        pass
