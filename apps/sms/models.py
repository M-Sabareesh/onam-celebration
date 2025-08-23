from django.db import models

# Placeholder for SMS models
# Add your SMS service models here

class SMSLog(models.Model):
    """Placeholder SMS log model"""
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"SMS to {self.phone_number}"
