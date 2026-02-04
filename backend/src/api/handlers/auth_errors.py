from fastapi import HTTPException, status, Request, Response
from fastapi.responses import JSONResponse


async def jwt_validation_error_handler(request: Request, exc: HTTPException) -> Response:
    """
    Global error handler for JWT validation errors.
    Returns consistent error responses for authentication and authorization failures.
    """
    # Map HTTPException status codes to appropriate responses
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": exc.detail if exc.detail else "Unauthorized: Invalid or missing credentials",
                "error_code": "AUTH_401"
            }
        )
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": exc.detail if exc.detail else "Forbidden: Insufficient permissions",
                "error_code": "AUTH_403"
            }
        )
    else:
        # For other HTTP exceptions, return the original exception
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail if exc.detail else "Authentication error",
                "error_code": "AUTH_ERR"
            }
        )


def register_auth_error_handlers(app):
    """
    Register authentication-related error handlers with the FastAPI application.
    """
    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        # Only handle authentication/authorization related HTTP exceptions
        if exc.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]:
            return await jwt_validation_error_handler(request, exc)
        # For other HTTP exceptions, re-raise to let other handlers deal with them
        raise exc