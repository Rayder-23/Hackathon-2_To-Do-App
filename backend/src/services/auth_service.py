from datetime import datetime
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
import os
from ..config import Config
from datetime import timezone, datetime, timedelta

def verify_token(token: str) -> Optional[dict]:
    """
    Verify a BetterAuth JWT token and return the payload if valid.
    This function validates JWT tokens issued by BetterAuth and verifies required claims.
    Uses the sub claim as the sole authoritative user identity.
    """
    try:
        # Decode the JWT token using the secret from configuration
        payload = jwt.decode(
            token,
            Config.BETTER_AUTH_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
            options={
                "require": ["sub", "exp", "iat"],
                "verify_exp": True,
                "verify_iat": True,
            },
            # Add clock skew tolerance of 5 seconds as specified
            leeway=timedelta(seconds=Config.JWT_CLOCK_SKEW_TOLERANCE)
        )

        # Extract the sub claim which is the authoritative user identifier
        user_sub = payload.get("sub")
        if not user_sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing required 'sub' claim"
            )

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTClaimsError as e:
        # Specific claim validation errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token claims: {str(e)}"
        )
    except JWTError as e:
        # Handle various JWT errors as per RFC 7807 Problem Details
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )





def get_user_identity_from_token(token: str) -> str:
    """
    Extract user identity exclusively from the verified JWT 'sub' claim.
    This implements the zero-trust approach where user identity is derived solely from verified JWT claims.
    Returns the user identifier from the 'sub' claim.
    """
    payload = verify_token(token)

    # Use ONLY the 'sub' claim as the authoritative user identity
    user_sub: str = payload.get("sub")
    if user_sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing required 'sub' claim"
        )

    return user_sub