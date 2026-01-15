from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
import os
from sqlmodel import Session
from ..models.user import User
from ..database.session import get_session

# Secret key for JWT verification - should come from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", os.getenv("JWT_SECRET", "fallback-secret-key"))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 24 hours as specified in the requirements

def verify_token(token: str) -> Optional[dict]:
    """
    Verify a BetterAuth JWT token and return the payload if valid.
    This function validates JWT tokens issued by BetterAuth and verifies required claims.
    """
    try:
        print(f"Attempting to decode token: {token[:20]}...")  # Log first 20 chars for debugging
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")

        # BetterAuth tokens might have different claim structures
        # Check for various possible identifiers
        user_identifier = payload.get("email") or payload.get("sub") or payload.get("id")
        if not user_identifier:
            print("Token missing required user identifier")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing required user identifier"
            )

        # Check if token is expired
        exp = payload.get("exp")
        if exp and exp < datetime.utcnow().timestamp():
            print("Token has expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        print("Token validation successful")
        return payload
    except JWTError as e:
        # Log the specific JWT error for debugging
        print(f"JWT Error: {str(e)}")
        # Handle various JWT errors as per RFC 7807 Problem Details
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the given data.
    This function generates JWT tokens that are compatible with BetterAuth expectations.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 24 hours as specified in requirements
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_from_token(
    token: str,
    db: Session
) -> User:
    """
    Get current user from BetterAuth JWT token.
    Implements zero-trust approach by deriving user identity exclusively from verified JWT claims.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    email: str = payload.get("email")
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user