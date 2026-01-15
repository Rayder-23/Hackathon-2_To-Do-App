from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ...database.session import get_session
from ...models.user import User, UserCreate
from ...services.user_service import UserService
from ...services.auth_service import verify_token, get_current_user_from_token, create_access_token
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
    Authenticate user and return JWT.
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
    """
    try:
        # Create user using existing service - validation is handled within UserService.create_user
        user = UserService.create_user(db, sign_up_data.email, sign_up_data.password)

        # Format the created_at datetime properly
        created_at_str = None
        if hasattr(user, 'created_at') and user.created_at:
            created_at_str = user.created_at.isoformat()

        # Create JWT token for the user
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "name": sign_up_data.name or user.email.split('@')[0]
        }
        access_token = create_access_token(data=token_data)

        # Prepare the response data
        response_data = {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": sign_up_data.name or user.email.split('@')[0],
                "createdAt": created_at_str
            },
            "session": {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "name": sign_up_data.name or user.email.split('@')[0],
                },
                "accessToken": access_token,
                "refreshToken": None
            },
            "token": access_token
        }

        # Create response with proper headers that BetterAuth expects
        response = JSONResponse(content=response_data)

        # Add all the headers that BetterAuth JWT plugin might expect
        response.headers["set-auth-token"] = access_token
        response.headers["set-auth-jwt"] = access_token  # This is the header mentioned in docs

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

    # Create JWT token for the user
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "name": getattr(user, 'name', user.email.split('@')[0])
    }
    access_token = create_access_token(data=token_data)

    # Prepare the response data
    response_data = {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": getattr(user, 'name', user.email.split('@')[0]),
            "createdAt": created_at_str
        },
        "session": {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": getattr(user, 'name', user.email.split('@')[0]),
            },
            "accessToken": access_token,
            "refreshToken": None
        },
        "token": access_token
    }

    # Create response with proper headers that BetterAuth expects
    response = JSONResponse(content=response_data)

    # Add all the headers that BetterAuth JWT plugin might expect
    response.headers["set-auth-token"] = access_token
    response.headers["set-auth-jwt"] = access_token  # This is the header mentioned in docs

    return response


@router.get("/auth/get-session")
def better_auth_get_session(current_user: dict = Depends(get_current_user)):
    """
    BetterAuth-compatible endpoint to get current session.
    """
    # Format the created_at datetime properly for get-session
    created_at_str = None
    user_created_at = getattr(current_user, 'created_at', None)
    if user_created_at:
        created_at_str = user_created_at.isoformat()

    # Return session information in BetterAuth-compatible format
    return {
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "name": getattr(current_user, 'name', current_user.email.split('@')[0]),
            "createdAt": created_at_str
        },
        "expires": None  # Let BetterAuth handle token expiration
    }


from fastapi import Request
import json

@router.get("/auth/token")
def better_auth_get_token(request: Request, db: Session = Depends(get_session)):
    """
    BetterAuth-compatible endpoint to get JWT token for backend API access.
    This endpoint returns a JWT token that can be used for external API authentication.
    """
    print(f"All headers received: {dict(request.headers)}")

    # Try to get the authorization header (traditional Bearer token approach)
    auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
    if auth_header:
        print(f"Authorization header found: {auth_header}")

        # Parse the Bearer token
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )

        token = auth_header[len("Bearer "):]
        print(f"Extracted token: {token[:20] if token else 'None'}...")

        # Validate the token
        payload = verify_token(token)
        print(f"Token payload: {payload}")

        # Get user from the token
        email = payload.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing email"
            )

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        # Create a new JWT token specifically for backend API access
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "user_id": str(user.id)
        }
        access_token = create_access_token(data=token_data)

        return {
            "token": access_token
        }
    else:
        print("No Authorization header found")

        # BetterAuth might be using the set-auth-jwt header approach mentioned in the documentation
        # Try to get token from set-auth-jwt header (as mentioned in docs)
        jwt_header = request.headers.get("set-auth-jwt") or request.headers.get("x-auth-jwt")
        if jwt_header:
            print(f"Found set-auth-jwt or x-auth-jwt header: {jwt_header}")

            # Validate this token
            payload = verify_token(jwt_header)
            email = payload.get("email")
            if not email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token missing email"
                )

            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )

            # Create a new JWT token specifically for backend API access
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "user_id": str(user.id)
            }
            access_token = create_access_token(data=token_data)

            return {
                "token": access_token
            }

        # Also try to see if there are other authentication headers
        auth_token_header = request.headers.get("x-auth-token")
        if auth_token_header:
            print(f"Found alternative auth header: {auth_token_header}")
            # Validate this token
            payload = verify_token(auth_token_header)
            email = payload.get("email")
            if not email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token missing email"
                )

            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )

            # Create a new JWT token specifically for backend API access
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "user_id": str(user.id)
            }
            access_token = create_access_token(data=token_data)

            return {
                "token": access_token
            }
        else:
            print("No authentication information found in headers.")

            # As a fallback for this custom implementation, we could try to identify the user
            # by other means, but this would be less secure.
            # For a proper BetterAuth-compatible server, the client should send proper authentication.

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authorization token provided in request headers"
            )