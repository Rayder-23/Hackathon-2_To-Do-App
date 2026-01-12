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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verify required claims exist as specified in FR-016
        required_claims = ["sub", "email", "exp", "iat"]
        for claim in required_claims:
            if claim not in payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token missing required claims"
                )

        # Check if token is expired
        if payload["exp"] < datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        return payload
    except JWTError:
        # Handle various JWT errors as per RFC 7807 Problem Details
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def create_access_token(data: dict):
    """
    Create a JWT access token with the provided data.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp(), "iat": datetime.utcnow().timestamp()})
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