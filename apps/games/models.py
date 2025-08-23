from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Placeholder for games models
# Add your treasure hunt game models here

class Game(models.Model):
    """Placeholder Game model"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
