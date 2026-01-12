from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from typing import Optional
import time
from collections import defaultdict

# Initialize limiter for IP-based rate limiting
limiter = Limiter(key_func=get_remote_address)

# In-memory storage for user-based rate limiting
user_rate_limits = defaultdict(list)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware to handle rate limiting per user and per IP.
    Implements FR-015: System MUST implement rate limiting of 100 requests per hour per IP address
    AND 500 requests per hour per authenticated user to prevent abuse.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Get user from request if authenticated (extract from JWT in Authorization header)
        user_id = self.extract_user_id_from_request(request)

        # Check IP-based rate limit (100 requests per hour)
        if not self.check_ip_rate_limit(request):
            from fastapi.responses import JSONResponse
            from fastapi import status

            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded: 100 requests per hour per IP address"}
            )

        # Check user-based rate limit (500 requests per hour) if user is authenticated
        if user_id and not self.check_user_rate_limit(user_id):
            from fastapi.responses import JSONResponse
            from fastapi import status

            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": f"Rate limit exceeded: 500 requests per hour per authenticated user (user {user_id})"}
            )

        response = await call_next(request)
        return response

    def extract_user_id_from_request(self, request: Request) -> Optional[str]:
        """
        Extract user ID from JWT token in Authorization header.
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header[7:]  # Remove "Bearer " prefix

        # Import here to avoid circular imports
        from jose import jwt
        import os

        SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", os.getenv("JWT_SECRET", "fallback-secret-key"))
        ALGORITHM = "HS256"

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            return user_id
        except Exception:
            # If token is invalid, return None (unauthenticated)
            return None

    def check_ip_rate_limit(self, request: Request) -> bool:
        """
        Check if IP address has exceeded rate limit (100 requests per hour).
        """
        client_ip = get_remote_address(request)

        # Get current time
        now = time.time()
        one_hour = 3600  # seconds in an hour

        # Get request timestamps for this IP
        ip_requests = getattr(self, '_ip_requests', {})
        if client_ip not in ip_requests:
            ip_requests[client_ip] = []

        # Filter requests from the last hour
        recent_requests = [req_time for req_time in ip_requests[client_ip] if now - req_time < one_hour]
        ip_requests[client_ip] = recent_requests

        # Store updated requests
        self._ip_requests = ip_requests

        # Check if limit is exceeded
        if len(recent_requests) >= 100:  # 100 requests per hour per IP
            return False

        # Add current request
        ip_requests[client_ip].append(now)
        self._ip_requests = ip_requests

        return True

    def check_user_rate_limit(self, user_id: str) -> bool:
        """
        Check if user has exceeded rate limit (500 requests per hour).
        """
        now = time.time()
        one_hour = 3600  # seconds in an hour

        # Get request timestamps for this user
        user_requests = user_rate_limits[user_id]

        # Filter requests from the last hour
        recent_requests = [req_time for req_time in user_requests if now - req_time < one_hour]
        user_rate_limits[user_id] = recent_requests

        # Check if limit is exceeded
        if len(recent_requests) >= 500:  # 500 requests per hour per user
            return False

        # Add current request
        user_rate_limits[user_id].append(now)

        return True