"""URLs for authentication endpoints"""
from django.urls import path
from core.auth_views import (
    phone_request_otp,
    phone_verify_otp,
    email_register,
    email_login,
    google_login,
    health,
)

urlpatterns = [
    # Health check
    path('health/', health, name='health'),
    
    # Phone authentication
    path('auth/phone/request-otp/', phone_request_otp, name='phone_request_otp'),
    path('auth/phone/verify-otp/', phone_verify_otp, name='phone_verify_otp'),
    
    # Email authentication
    path('auth/email/register/', email_register, name='email_register'),
    path('auth/email/login/', email_login, name='email_login'),
    
    # Google authentication
    path('auth/google/login/', google_login, name='google_login'),
]
