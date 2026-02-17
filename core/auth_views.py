"""Authentication API views"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.auth_service import (
    login_email,
    login_google,
    register_email,
    request_phone_otp,
    verify_phone_otp,
)
from core.serializers import (
    EmailAuthOutSerializer,
    EmailLoginInSerializer,
    EmailRegisterInSerializer,
    GoogleAuthOutSerializer,
    GoogleLoginInSerializer,
    PhoneRequestOtpInSerializer,
    PhoneRequestOtpOutSerializer,
    PhoneVerifyOtpInSerializer,
    PhoneVerifyOtpOutSerializer,
    TokenResponseSerializer,
    UserResponseSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def phone_request_otp(request):
    """Request OTP for phone authentication"""
    serializer = PhoneRequestOtpInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        challenge_data, debug_otp = request_phone_otp(serializer.validated_data['phone'])
        response_serializer = PhoneRequestOtpOutSerializer(challenge_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def phone_verify_otp(request):
    """Verify OTP and authenticate user"""
    serializer = PhoneVerifyOtpInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        token, user = verify_phone_otp(
            serializer.validated_data['challenge_id'],
            serializer.validated_data['otp']
        )
        
        response_data = {
            'token': {
                'access_token': token,
                'token_type': 'bearer'
            },
            'user': {
                'id': str(user.id)
            }
        }
        response_serializer = PhoneVerifyOtpOutSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def email_register(request):
    """Register user with email and password"""
    serializer = EmailRegisterInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        token, user = register_email(
            serializer.validated_data['email'],
            serializer.validated_data['password']
        )
        
        response_data = {
            'token': {
                'access_token': token,
                'token_type': 'bearer'
            },
            'user': {
                'id': str(user.id)
            }
        }
        response_serializer = EmailAuthOutSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def email_login(request):
    """Login user with email and password"""
    serializer = EmailLoginInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        token, user = login_email(
            serializer.validated_data['email'],
            serializer.validated_data['password']
        )
        
        response_data = {
            'token': {
                'access_token': token,
                'token_type': 'bearer'
            },
            'user': {
                'id': str(user.id)
            }
        }
        response_serializer = EmailAuthOutSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """Login user with Google ID token"""
    serializer = GoogleLoginInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        token, user = login_google(serializer.validated_data['id_token'])
        
        response_data = {
            'token': {
                'access_token': token,
                'token_type': 'bearer'
            },
            'user': {
                'id': str(user.id)
            }
        }
        response_serializer = GoogleAuthOutSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    """Health check endpoint"""
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)
