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
    # Extract user_id from path - the pattern is /api/{user_id}/tasks
    path_parts = request.url.path.strip('/').split('/')

    # Look for the user_id in the path (should be after 'api')
    if 'api' in path_parts:
        api_index = path_parts.index('api')
        if api_index + 1 < len(path_parts):
            # The next part after 'api' should be the user_id
            requested_user_id = path_parts[api_index + 1]

            # Validate that requested_user_id is numeric
            if requested_user_id.isdigit():
                if jwt_sub != requested_user_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied: You can only access your own resources"
                    )

    return jwt_sub