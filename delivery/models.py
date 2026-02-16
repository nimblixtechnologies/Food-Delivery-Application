from django.db import models
from django.conf import settings

class DeliveryProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery_profile')
    is_available = models.BooleanField(default=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery Partner: {self.user.username}"
