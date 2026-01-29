# Quickstart Guide: Backend-Frontend Authentication Alignment

## Setup

### 1. Environment Variables
```bash
# Set the shared secret used by both frontend and backend
export BETTER_AUTH_SECRET="your-secret-key-here"

# Backend configuration
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

### 2. Install Dependencies
```bash
# Backend dependencies
cd backend
pip install fastapi sqlmodel python-jose cryptography

# Frontend dependencies (already handled by Better Auth)
cd frontend
npm install @better-auth/client
```

## Implementation Overview

### 1. JWT Validation Service
```python
# backend/src/services/auth_service.py
from jose import JWTError, jwt
from typing import Optional

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload if valid."""
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"],
            options={"verify_exp": True, "clock_skew": 5}
        )
        return payload
    except JWTError:
        return None
```

### 2. Authentication Dependency
```python
# backend/src/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from typing import Dict

async def get_current_user(authorization: str = Header(...)) -> Dict:
    """Dependency to get current user from JWT token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    user_payload = verify_token(token)

    if not user_payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Verify required claims exist
    required_claims = {"sub", "exp", "iat"}
    if not required_claims.issubset(user_payload.keys()):
        raise HTTPException(status_code=401, detail="Missing required claims")

    return user_payload
```

### 3. User Identity Enforcement
```python
# backend/src/api/routes/users.py
@app.get("/api/users/{user_id}/tasks")
async def get_user_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get tasks for authenticated user only."""
    # Verify JWT sub matches URL user_id
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    # Query user's tasks only
    tasks = await get_user_tasks_from_db(user_id)
    return {"tasks": tasks}
```

## Testing

### 1. JWT Validation Tests
```bash
# Test valid token
curl -H "Authorization: Bearer <valid_token>" http://localhost:8000/api/users/user123/tasks

# Test invalid token
curl -H "Authorization: Bearer <invalid_token>" http://localhost:8000/api/users/user123/tasks

# Test missing token
curl http://localhost:8000/api/users/user123/tasks
```

### 2. Cross-User Access Tests
```bash
# Authenticate as user1, get token
# Try to access user2's data with user1's token (should fail with 403)
curl -H "Authorization: Bearer <user1_token>" http://localhost:8000/api/users/user2/tasks
```

## Security Considerations

1. **Always validate JWT signature** before trusting any claims
2. **Enforce 5-second clock skew tolerance** for expiration validation
3. **Verify all required claims exist** before processing request
4. **Compare JWT sub claim with URL user_id** to prevent cross-user access
5. **Log all authentication failures** for security monitoring
6. **Never accept user identity from sources other than verified JWT**

## Common Issues

### 1. Clock Skew Problems
- Symptom: Valid tokens occasionally rejected
- Solution: Ensure server clocks are synchronized and use 5-second tolerance

### 2. Cross-User Access
- Symptom: Users accessing other users' data
- Solution: Always compare JWT `sub` with URL `user_id`

### 3. Missing Claims
- Symptom: 401 errors despite valid authentication
- Solution: Verify Better Auth is configured to include required claims