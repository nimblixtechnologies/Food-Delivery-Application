"""Serializers for authentication endpoints"""
from rest_framework import serializers
from core.models import User, AuthIdentity


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'created_at']


class AuthIdentitySerializer(serializers.ModelSerializer):
    """Serializer for AuthIdentity model"""
    class Meta:
        model = AuthIdentity
        fields = ['id', 'provider', 'email', 'phone', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified']


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response"""
    access_token = serializers.CharField()
    token_type = serializers.CharField(default='bearer', read_only=True)


class UserResponseSerializer(serializers.Serializer):
    """Serializer for user response"""
    id = serializers.CharField()


# Phone Authentication Serializers
class PhoneRequestOtpInSerializer(serializers.Serializer):
    """Request OTP for phone authentication"""
    phone = serializers.CharField(min_length=6, max_length=32)


class PhoneRequestOtpOutSerializer(serializers.Serializer):
    """Response after requesting OTP"""
    challenge_id = serializers.CharField()
    expires_in = serializers.IntegerField()
    debug_otp = serializers.CharField(required=False, allow_null=True)


class PhoneVerifyOtpInSerializer(serializers.Serializer):
    """Verify OTP for phone authentication"""
    challenge_id = serializers.CharField()
    otp = serializers.CharField(min_length=4, max_length=10)


class PhoneVerifyOtpOutSerializer(serializers.Serializer):
    """Response after verifying OTP"""
    token = TokenResponseSerializer()
    user = UserResponseSerializer()


# Email Authentication Serializers
class EmailRegisterInSerializer(serializers.Serializer):
    """Register with email and password"""
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=128)


class EmailAuthOutSerializer(serializers.Serializer):
    """Response after email authentication"""
    token = TokenResponseSerializer()
    user = UserResponseSerializer()


class EmailLoginInSerializer(serializers.Serializer):
    """Login with email and password"""
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=128)


# Google Authentication Serializers
class GoogleLoginInSerializer(serializers.Serializer):
    """Login with Google ID token"""
    id_token = serializers.CharField()


class GoogleAuthOutSerializer(serializers.Serializer):
    """Response after Google authentication"""
    token = TokenResponseSerializer()
    user = UserResponseSerializer()
