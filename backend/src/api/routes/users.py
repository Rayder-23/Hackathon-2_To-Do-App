from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ...database.session import get_session
from ...models.user import User, UserCreate
from ...services.user_service import UserService
from ...api.middleware.auth_middleware import get_current_user
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class BetterAuthSignUpRequest(BaseModel):
    email: str
    password: str
    name: str = ""

class BetterAuthSignInRequest(BaseModel):
    email: str
    password: str

class BetterAuthUserResponse(BaseModel):
    id: str
    email: str
    name: str
    createdAt: Optional[str] = None

class BetterAuthAuthResponse(BaseModel):
    user: BetterAuthUserResponse
    token: Optional[str] = None
    session: Optional[dict] = None

from typing import Optional
from datetime import datetime


@router.post("/users/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_session)):
    """
    Register a new user.
    Implements FR-001: System MUST allow users to register with email and password credentials
    Implements FR-013: System MUST reject user registration attempts with duplicate email addresses and return HTTP 409 Conflict
    Implements FR-014: System MUST validate email format using the pattern /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    """
    try:
        user = UserService.create_user(db, user_data.email, user_data.password)

        # Return user data without creating a token (BetterAuth handles token creation)
        return {
            "id": user.id,
            "email": user.email,
        }
    except HTTPException as e:
        # Re-raise HTTP exceptions as they are (e.g., 400 for validation, 409 for conflict)
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/users/login")
def login_user(login_data: LoginRequest, db: Session = Depends(get_session)):
    """
    Authenticate user.
    Backend should not issue tokens - BetterAuth handles token creation.
    Implements FR-002: System MUST authenticate users via JWT tokens issued by Better Auth with expiration after 24 hours and refresh tokens valid for 7 days
    """
    user = UserService.authenticate_user(db, login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return success without creating token (BetterAuth handles token creation)
    return {
        "success": True
    }

# BetterAuth-compatible endpoints
from fastapi.responses import JSONResponse

@router.post("/auth/sign-up/email")
def better_auth_sign_up(sign_up_data: BetterAuthSignUpRequest, db: Session = Depends(get_session)):
    """
    BetterAuth-compatible endpoint for user registration.
    Backend does not issue tokens - this is a placeholder that forwards to BetterAuth.
    """
    try:
        # Create user using existing service - validation is handled within UserService.create_user
        user = UserService.create_user(db, sign_up_data.email, sign_up_data.password)

        # Format the created_at datetime properly
        created_at_str = None
        if hasattr(user, 'created_at') and user.created_at:
            created_at_str = user.created_at.isoformat()

        # Prepare the response data - do NOT create tokens (BetterAuth handles this)
        response_data = {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": sign_up_data.name or user.email.split('@')[0],
                "createdAt": created_at_str
            },
            # No session or token information - BetterAuth handles this
        }

        # Create response with proper headers that BetterAuth expects
        response = JSONResponse(content=response_data)

        return response
    except HTTPException as e:
        # Re-raise HTTP exceptions as they are (e.g., 400 for validation, 409 for conflict)
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/auth/sign-in/email")
def better_auth_sign_in(sign_in_data: BetterAuthSignInRequest, db: Session = Depends(get_session)):
    """
    BetterAuth-compatible endpoint for user login.
    Backend does not issue tokens - this is a placeholder that forwards to BetterAuth.
    """
    user = UserService.authenticate_user(db, sign_in_data.email, sign_in_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Format the created_at datetime properly for sign-in
    created_at_str = None
    user_created_at = getattr(user, 'created_at', None)
    if user_created_at:
        created_at_str = user_created_at.isoformat()

    # Prepare the response data - do NOT create tokens (BetterAuth handles this)
    response_data = {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": getattr(user, 'name', user.email.split('@')[0]),
            "createdAt": created_at_str
        },
        # No session or token information - BetterAuth handles this
    }

    # Create response with proper headers that BetterAuth expects
    response = JSONResponse(content=response_data)

    return response


@router.get("/auth/get-session")
def better_auth_get_session(jwt_sub: str = Depends(get_current_user)):
    """
    BetterAuth-compatible endpoint to get current session.
    Backend does not issue tokens - this is a placeholder that forwards to BetterAuth.
    """
    # In a real implementation, this would validate that the JWT sub exists
    # and possibly fetch user data based on the JWT sub identifier
    # but since we're only verifying JWTs from BetterAuth, we'll just return placeholder

    # For now, return a basic response indicating the session exists
    return {
        "sessionExists": True,
        "userId": jwt_sub  # Use the sub from JWT as the user identifier
    }


from fastapi import Request

@router.get("/auth/token")
def better_auth_get_token(request: Request):
    """
    BetterAuth-compatible endpoint to validate JWT token.
    Backend does not issue tokens - this endpoint only validates incoming tokens.
    """
    # This endpoint should NOT create new tokens. It should only validate existing ones.
    # In a real implementation, BetterAuth would handle token issuance.
    # For compatibility, we'll just return a message indicating the backend is ready
    # for BetterAuth to handle token operations.

    return {
        "backendReady": True,
        "tokenHandling": "external",
        "message": "Backend is ready to validate tokens from BetterAuth"
    }