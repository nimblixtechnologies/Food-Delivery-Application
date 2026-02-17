"""Security utilities for authentication"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta

from jose import jwt

from passlib.context import CryptContext
from django.conf import settings

_pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using pbkdf2_sha256"""
    return _pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return _pwd_context.verify(password, password_hash)


def create_access_token(user_id: str) -> str:
    """Create JWT access token"""
    jwt_secret = getattr(settings, 'JWT_SECRET', 'change_me')
    jwt_alg = getattr(settings, 'JWT_ALG', 'HS256')
    jwt_expires_minutes = getattr(settings, 'JWT_EXPIRES_MINUTES', 60)
    
    now = datetime.utcnow()
    exp = now + timedelta(minutes=jwt_expires_minutes)
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp())
    }
    return jwt.encode(payload, jwt_secret, algorithm=jwt_alg)


def generate_otp() -> str:
    """Generate a random 6-digit OTP"""
    return f"{secrets.randbelow(1_000_000):06d}"


def otp_hash(phone: str, otp: str) -> str:
    """Hash OTP with phone number using HMAC-SHA256"""
    otp_secret = getattr(settings, 'OTP_SECRET', 'change_me')
    msg = f"{phone}:{otp}".encode("utf-8")
    key = otp_secret.encode("utf-8")
    digest = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return digest


def verify_jwt_token(token: str) -> dict:
    """Verify and decode JWT token"""
    jwt_secret = getattr(settings, 'JWT_SECRET', 'change_me')
    jwt_alg = getattr(settings, 'JWT_ALG', 'HS256')
    
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[jwt_alg])
        return payload
    except Exception:
        return None
