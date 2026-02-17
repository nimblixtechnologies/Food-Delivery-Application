# Authentication Service Integration

This document describes the new authentication service integrated into the Food Delivery Application.

## Overview

The authentication service provides multiple authentication methods:
- **Phone OTP**: One-time password verification via phone number
- **Email/Password**: Traditional email and password registration and login
- **Google OAuth**: Google ID token-based authentication

## API Endpoints

### Health Check
- `GET /api/auth/health/` - Health check endpoint

### Phone Authentication
- `POST /api/auth/auth/phone/request-otp/` - Request OTP for phone number
  - Request: `{"phone": "1234567890"}`
  - Response: `{"challenge_id": "uuid", "expires_in": 300, "debug_otp": "123456"}`

- `POST /api/auth/auth/phone/verify-otp/` - Verify OTP
  - Request: `{"challenge_id": "uuid", "otp": "123456"}`
  - Response: `{"token": {"access_token": "jwt", "token_type": "bearer"}, "user": {"id": "uuid"}}`

### Email Authentication
- `POST /api/auth/auth/email/register/` - Register with email and password
  - Request: `{"email": "user@example.com", "password": "password123"}`
  - Response: `{"token": {"access_token": "jwt", "token_type": "bearer"}, "user": {"id": "uuid"}}`

- `POST /api/auth/auth/email/login/` - Login with email and password
  - Request: `{"email": "user@example.com", "password": "password123"}`
  - Response: `{"token": {"access_token": "jwt", "token_type": "bearer"}, "user": {"id": "uuid"}}`

### Google Authentication
- `POST /api/auth/auth/google/login/` - Login with Google ID token
  - Request: `{"id_token": "google_id_token"}`
  - Response: `{"token": {"access_token": "jwt", "token_type": "bearer"}, "user": {"id": "uuid"}}`

## Environment Variables

Configure the following environment variables in your `.env` file:

```
JWT_SECRET=your-secret-key
JWT_ALG=HS256
JWT_EXPIRES_MINUTES=60

OTP_SECRET=your-otp-secret
OTP_TTL_SECONDS=300
OTP_DEBUG_RETURN=True

GOOGLE_CLIENT_ID=your-google-client-id
```

## Database Models

### User
- `id` (UUID): Primary key
- `created_at` (DateTime): User creation timestamp

### AuthIdentity
- `id` (UUID): Primary key
- `user_id` (FK): Reference to User
- `provider` (Enum): Authentication provider (phone, email, google)
- `email` (String, nullable, unique): Email address
- `phone` (String, nullable, unique): Phone number
- `provider_user_id` (String, nullable): External provider user ID
- `password_hash` (String, nullable): Hashed password
- `is_verified` (Boolean): Verification status
- `created_at` (DateTime): Creation timestamp

### OtpChallenge
- `id` (UUID): Primary key
- `phone` (String): Phone number
- `otp_hash` (String): Hashed OTP
- `expires_at` (DateTime): OTP expiration time
- `attempts` (Integer): Failed attempt count
- `created_at` (DateTime): Creation timestamp

## Setup Instructions

1. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update .env with your configuration
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Files Modified/Created

### New Files:
- `core/auth_service.py` - Authentication business logic
- `core/security.py` - JWT and password utilities
- `core/serializers.py` - DRF serializers for auth endpoints
- `core/auth_views.py` - API views for authentication
- `core/auth_urls.py` - URL routing for auth endpoints
- `requirements.txt` - Python dependencies

### Modified Files:
- `core/models.py` - Added User, AuthIdentity, OtpChallenge models
- `food_delivery/settings.py` - Added authentication configuration
- `food_delivery/urls.py` - Added auth URLs to the main route

## Testing

You can test the endpoints using curl. Here are all the test commands:

### 1. Health Check
```bash
curl -X GET http://localhost:8000/api/auth/health/
```

**Expected Response:**
```json
{"status":"ok"}
```

### 2. Phone OTP - Request OTP
```bash
curl -X POST http://localhost:8000/api/auth/auth/phone/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

**Expected Response:**
```json
{
  "challenge_id": "a7e297d9-320f-4ce7-98a7-1fa1d57ca8fd",
  "expires_in": 300,
  "debug_otp": "125852"
}
```

### 3. Phone OTP - Verify OTP
```bash
curl -X POST http://localhost:8000/api/auth/auth/phone/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"challenge_id": "a7e297d9-320f-4ce7-98a7-1fa1d57ca8fd", "otp": "125852"}'
```

**Expected Response:**
```json
{
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "user": {
    "id": "815df487-06f3-46a7-ad29-d271dd7a0bb8"
  }
}
```

### 4. Email Registration
```bash
curl -X POST http://localhost:8000/api/auth/auth/email/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

**Expected Response:**
```json
{
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "user": {
    "id": "7d8d0d09-4ee8-487b-aaac-a8f43081c589"
  }
}
```

### 5. Email Login
```bash
curl -X POST http://localhost:8000/api/auth/auth/email/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

**Expected Response:**
```json
{
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "user": {
    "id": "7d8d0d09-4ee8-487b-aaac-a8f43081c589"
  }
}
```

### 6. Google Login (requires valid Google ID token)
```bash
curl -X POST http://localhost:8000/api/auth/auth/google/login/ \
  -H "Content-Type: application/json" \
  -d '{"id_token": "YOUR_GOOGLE_ID_TOKEN"}'
```

**Expected Response:**
```json
{
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "user": {
    "id": "google-user-id-uuid"
  }
}
```

### Testing Full OTP Flow (Automated)
```bash
# Request OTP
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/auth/phone/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone": "+9876543210"}')

# Extract challenge_id and debug_otp using python
CHALLENGE_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['challenge_id'])")
DEBUG_OTP=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['debug_otp'])")

echo "Challenge ID: $CHALLENGE_ID"
echo "Debug OTP: $DEBUG_OTP"

# Verify OTP
curl -s -X POST http://localhost:8000/api/auth/auth/phone/verify-otp/ \
  -H "Content-Type: application/json" \
  -d "{\"challenge_id\": \"$CHALLENGE_ID\", \"otp\": \"$DEBUG_OTP\"}" | python3 -m json.tool
```



## Security Considerations

- JWT tokens are signed with `JWT_SECRET` - keep this secure
- OTP hashes use `OTP_SECRET` - keep this secure
- Passwords are hashed using pbkdf2_sha256
- All authentication endpoints are CSRF-exempt and allow unauthenticated access
- OTP has a 5-attempt limit
- OTP expires after the configured TTL (default: 300 seconds)
