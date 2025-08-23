from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
import uuid


class User(AbstractUser):
    """
    Custom User model with Swedish phone number support.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Remove username field
    email = models.EmailField(_('email address'), blank=True, null=True)
    phone_number = PhoneNumberField(
        _('phone number'),
        unique=True,
        region='SE',
        help_text=_('Enter Swedish phone number in format +46XXXXXXXXX')
    )
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    
    # Phone verification
    is_phone_verified = models.BooleanField(default=False)
    phone_verification_code = models.CharField(max_length=6, blank=True, null=True)
    phone_verification_sent_at = models.DateTimeField(blank=True, null=True)
    
    # Game stats
    total_score = models.PositiveIntegerField(default=0)
    games_completed = models.PositiveIntegerField(default=0)
    current_level = models.PositiveIntegerField(default=1)
    
    # Profile
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'accounts_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    def __str__(self):
        return str(self.phone_number)
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    @property
    def display_name(self):
        """Return display name for UI."""
        full_name = self.get_full_name()
        return full_name if full_name else str(self.phone_number)


class PhoneVerification(models.Model):
    """
    Model to track phone verification attempts.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_attempts')
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'accounts_phone_verification'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.phone_number} - {self.verification_code}"


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Preferences
    receive_sms_notifications = models.BooleanField(default=True)
    receive_game_updates = models.BooleanField(default=True)
    preferred_language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('sv', 'Swedish'),
            ('ml', 'Malayalam'),
        ],
        default='en'
    )
    
    # Social
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Game preferences
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_user_profile'
        
    def __str__(self):
        return f"{self.user.display_name}'s Profile"
