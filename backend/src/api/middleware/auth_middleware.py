from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlmodel import Session
from ...models.user import User
from ...database.session import get_session
from ...services.auth_service import get_current_user_from_token


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
) -> User:
    """
    Get the current authenticated user from the BetterAuth JWT token.
    This function enforces the zero-trust approach by deriving user identity
    exclusively from verified JWT claims from BetterAuth.
    """
    token = credentials.credentials
    return get_current_user_from_token(token, db)


def verify_user_access(user: User, requested_user_id: int) -> bool:
    """
    Verify that the authenticated user can access resources for the requested user ID.
    This enforces that users can only access their own tasks.
    """
    return user.id == requested_user_id


def verify_user_access_middleware(
    request: Request,
    user: User = Depends(get_current_user)
) -> User:
    """
    Middleware to verify user access to resources.
    Checks if URL user_id matches authenticated JWT user identity.
    Implements FR-022: System MUST reject requests where URL user_id does not match authenticated JWT user identity
    """
    # Extract user_id from path if it exists
    path_parts = request.url.path.split('/')
    user_id_pos = -1

    # Look for user_id in the path (e.g., /api/{user_id}/tasks)
    for i, part in enumerate(path_parts):
        if part.isdigit():  # If this part is a number, it might be the user_id
            # Check if the previous part was likely a user identifier
            if i > 0 and path_parts[i-1] in ['users', 'user', 'api']:
                user_id_pos = i
                break

    if user_id_pos != -1:
        try:
            requested_user_id = int(path_parts[user_id_pos])
            if user.id != requested_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: You can only access your own resources"
                )
        except ValueError:
            # If the path part is not a valid integer, ignore it
            pass

    return user