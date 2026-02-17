import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthProvider(models.TextChoices):
    PHONE = 'phone', 'Phone'
    EMAIL = 'email', 'Email'
    GOOGLE = 'google', 'Google'


class User(models.Model):
    """User model integrated with multi-auth support"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auth_users'
    
    def __str__(self):
        return str(self.id)


class AuthIdentity(models.Model):
    """Multi-provider authentication identity"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='identities')
    
    provider = models.CharField(max_length=20, choices=AuthProvider.choices)
    
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length=32, null=True, blank=True, unique=True)
    provider_user_id = models.CharField(max_length=255, null=True, blank=True)
    
    password_hash = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auth_identities'
        unique_together = ('provider', 'provider_user_id')
    
    def __str__(self):
        return f"{self.provider}:{self.email or self.phone}"


class OtpChallenge(models.Model):
    """OTP challenge for phone authentication"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=32)
    otp_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auth_otp_challenges'
    
    def __str__(self):
        return f"OTP:{self.phone}"
