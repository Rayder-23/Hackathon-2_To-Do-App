from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ...services.auth_service import get_user_identity_from_token


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current authenticated user identity from the BetterAuth JWT token.
    This function enforces the zero-trust approach by deriving user identity
    exclusively from verified JWT claims from BetterAuth.
    Returns the user identifier from the 'sub' claim.
    """
    token = credentials.credentials
    return get_user_identity_from_token(token)


def verify_user_access(jwt_sub: str, requested_user_id: str) -> bool:
    """
    Verify that the authenticated user can access resources for the requested user ID.
    This enforces that users can only access their own tasks by comparing JWT 'sub' with URL user_id.
    """
    return jwt_sub == requested_user_id


def verify_user_access_middleware(
    request: Request,
    jwt_sub: str = Depends(get_current_user)
) -> str:
    """
    Middleware to verify user access to resources.
    Checks if URL user_id matches authenticated JWT 'sub' claim.
    Implements FR-022: System MUST reject requests where URL user_id does not match authenticated JWT user identity
    """
    # Extract user_id from path if it exists
    path_parts = request.url.path.split('/')

    # Look for user_id in the path (e.g., /api/{user_id}/tasks, /users/{user_id}/tasks)
    for i, part in enumerate(path_parts):
        if part.isdigit():  # If this part is a number, it might be the user_id
            # Check if the previous part indicates this is a user resource
            if i > 0 and path_parts[i-1] in ['users', 'user', 'api']:
                requested_user_id = part
                if jwt_sub != requested_user_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied: You can only access your own resources"
                    )
                break
            # Also check for other common patterns like /api/tasks/{user_id}/...
            elif i < len(path_parts) - 1 and path_parts[i+1] in ['tasks', 'task', 'todos']:
                requested_user_id = part
                if jwt_sub != requested_user_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied: You can only access your own resources"
                    )
                break

    return jwt_sub