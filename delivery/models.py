from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class DeliveryProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery_profile')
    is_available = models.BooleanField(default=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField(default=0.0)

class DeliveryRating(models.Model):
    # One review per specific order
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='delivery_rating')
    partner = models.ForeignKey(DeliveryProfile, on_delete=models.CASCADE, related_name='ratings')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Enforces 0-5 rating
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'order')