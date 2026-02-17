"""Authentication service with multi-provider support"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone as django_timezone
from rest_framework.exceptions import ValidationError
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from core.models import AuthIdentity, AuthProvider, OtpChallenge, User
from core.security import (
    create_access_token,
    generate_otp,
    hash_password,
    otp_hash,
    verify_password,
)


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _normalize_phone(phone: str) -> str:
    return phone.strip()


def _validate_bcrypt_password_len(password: str) -> None:
    if len(password.encode("utf-8")) > 72:
        raise ValidationError("Password too long")


def request_phone_otp(phone: str) -> Tuple[dict, Optional[str]]:
    """Request OTP for phone authentication"""
    phone_n = _normalize_phone(phone)
    otp = generate_otp()
    now = django_timezone.now()
    
    otp_ttl_seconds = getattr(settings, 'OTP_TTL_SECONDS', 300)
    
    challenge = OtpChallenge.objects.create(
        phone=phone_n,
        otp_hash=otp_hash(phone_n, otp),
        expires_at=now + timedelta(seconds=otp_ttl_seconds),
        attempts=0,
    )
    
    otp_debug_return = getattr(settings, 'OTP_DEBUG_RETURN', True)
    debug_otp = otp if otp_debug_return else None
    
    return {
        "challenge_id": str(challenge.id),
        "expires_in": otp_ttl_seconds,
        "debug_otp": debug_otp,
    }, debug_otp


def verify_phone_otp(challenge_id: str, otp: str) -> Tuple[str, User]:
    """Verify OTP and authenticate user"""
    try:
        challenge = OtpChallenge.objects.get(id=challenge_id)
    except OtpChallenge.DoesNotExist:
        raise ValidationError("Invalid challenge")
    
    if django_timezone.now() > challenge.expires_at:
        raise ValidationError("OTP expired")
    
    if challenge.attempts >= 5:
        raise ValidationError("Too many attempts")
    
    expected = otp_hash(challenge.phone, otp)
    if expected != challenge.otp_hash:
        challenge.attempts += 1
        challenge.save()
        raise ValidationError("Invalid OTP")
    
    # Get or create identity
    identity = AuthIdentity.objects.filter(
        provider=AuthProvider.PHONE,
        phone=challenge.phone,
    ).first()
    
    if identity:
        identity.is_verified = True
        identity.save()
        user = identity.user
    else:
        user = User.objects.create()
        identity = AuthIdentity.objects.create(
            user=user,
            provider=AuthProvider.PHONE,
            phone=challenge.phone,
            is_verified=True,
        )
    
    # Delete challenge
    challenge.delete()
    
    token = create_access_token(str(user.id))
    return token, user


def register_email(email: str, password: str) -> Tuple[str, User]:
    """Register user with email and password"""
    email_n = _normalize_email(email)
    _validate_bcrypt_password_len(password)
    
    # Check if email already exists
    if AuthIdentity.objects.filter(provider=AuthProvider.EMAIL, email=email_n).exists():
        raise ValidationError("Email already registered")
    
    # Create user and identity
    user = User.objects.create()
    identity = AuthIdentity.objects.create(
        user=user,
        provider=AuthProvider.EMAIL,
        email=email_n,
        password_hash=hash_password(password),
        is_verified=True,
    )
    
    token = create_access_token(str(user.id))
    return token, user


def login_email(email: str, password: str) -> Tuple[str, User]:
    """Login user with email and password"""
    email_n = _normalize_email(email)
    _validate_bcrypt_password_len(password)
    
    identity = AuthIdentity.objects.filter(
        provider=AuthProvider.EMAIL,
        email=email_n
    ).first()
    
    if not identity or not identity.password_hash:
        raise ValidationError("Invalid credentials")
    
    if not verify_password(password, identity.password_hash):
        raise ValidationError("Invalid credentials")
    
    token = create_access_token(str(identity.user_id))
    return token, identity.user


def login_google(id_token_str: str) -> Tuple[str, User]:
    """Login user with Google ID token"""
    google_client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
    if not google_client_id:
        raise ValidationError("Google login not configured")
    
    try:
        payload = google_id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            google_client_id,
        )
    except Exception:
        raise ValidationError("Invalid Google token")
    
    sub = payload.get("sub")
    if not sub:
        raise ValidationError("Invalid Google token")
    
    identity = AuthIdentity.objects.filter(
        provider=AuthProvider.GOOGLE,
        provider_user_id=sub,
    ).first()
    
    if identity:
        user = identity.user
    else:
        user = User.objects.create()
        identity = AuthIdentity.objects.create(
            user=user,
            provider=AuthProvider.GOOGLE,
            provider_user_id=sub,
            email=(payload.get("email") or "").lower() or None,
            is_verified=True,
        )
    
    token = create_access_token(str(user.id))
    return token, user
