from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

# Placeholder for Django signals
# Add your signal handlers here

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create user profile when a new user is created.
    This is a placeholder signal handler.
    """
    if created:
        # Add profile creation logic here when UserProfile model is ready
        pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save user profile when user is saved.
    This is a placeholder signal handler.
    """
    # Add profile saving logic here when UserProfile model is ready
    pass
