# Backend Structure Analysis Report

## Overview
Analysis of the current backend structure for the Todo App, focusing on authentication and authorization components.

## Directory Structure
```
backend/
├── src/
│   ├── api/
│   │   ├── middleware/
│   │   │   ├── auth_middleware.py          # Authentication and authorization middleware
│   │   │   └── rate_limit_middleware.py    # Rate limiting functionality
│   │   └── routes/
│   │       ├── tasks.py                    # Task-related API endpoints
│   │       └── users.py                    # User-related API endpoints (includes BetterAuth compatibility)
│   ├── database/
│   │   ├── migration.py                    # Database migration logic
│   │   └── session.py                      # Database session management
│   ├── models/
│   │   ├── base.py                         # Base SQLModel classes
│   │   ├── task.py                         # Task model definition
│   │   └── user.py                         # User model definition
│   ├── services/
│   │   ├── auth_service.py                 # Authentication service (includes JWT handling)
│   │   ├── task_service.py                 # Task business logic
│   │   └── user_service.py                 # User business logic
│   ├── todo-phase-1/                       # Legacy phase 1 code
│   │   ├── cli.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── services.py
│   │   └── __init__.py
│   └── main.py                             # FastAPI application entry point
```

## Authentication Components Analysis

### 1. auth_service.py
**Location**: `backend/src/services/auth_service.py`
- Contains JWT handling logic for both creating and verifying tokens
- Uses `jose` library for JWT operations
- Has both token creation and verification functions
- Currently has `create_access_token()` function which violates the requirement that "Backend does NOT issue tokens, manage sessions, or replicate Better Auth"
- Loads secret from `BETTER_AUTH_SECRET` environment variable

### 2. auth_middleware.py
**Location**: `backend/src/api/middleware/auth_middleware.py`
- Contains authentication and authorization middleware
- Extracts user from JWT token using `HTTPBearer`
- Implements `get_current_user()` function to extract user from token
- Contains `verify_user_access_middleware()` for comparing JWT `sub` claim with URL user_id
- Implements authorization enforcement by checking if authenticated user can access requested resources

### 3. users.py routes
**Location**: `backend/src/api/routes/users.py`
- Contains BetterAuth-compatible endpoints (`/auth/sign-up/email`, `/auth/sign-in/email`, etc.)
- **CRITICAL ISSUE**: Contains token creation logic (`create_access_token`) which violates the auth boundary specification
- Includes endpoints that issue JWTs, violating "Backend does NOT issue tokens, manage sessions, or replicate Better Auth"
- Has both traditional login/signup endpoints and BetterAuth compatibility endpoints

### 4. tasks.py routes
**Location**: `backend/src/api/routes/tasks.py`
- Properly implements authorization checking in all endpoints
- Uses dependency injection to get current user via `get_current_user`
- Verifies user access using `verify_user_access` function
- Implements proper ownership enforcement

## Redundant or Problematic Files

### 1. token creation in auth_service.py and users.py
**Issue**: The backend currently issues its own JWT tokens, which violates the specification that states "Backend does NOT issue tokens, manage sessions, or replicate Better Auth".

**Problem areas**:
- `auth_service.py:create_access_token()` function
- Multiple places in `users.py` that create tokens using `create_access_token()`

### 2. todo-phase-1 directory
**Issue**: Contains legacy code from Phase 1 that may be redundant.
**Status**: Appears to be historical/legacy code that might be safely removed.

## Issues Identified

### Critical Security Issues
1. **Auth Boundary Violation**: Backend is issuing JWT tokens instead of only verifying tokens from BetterAuth
2. **Role Confusion**: Backend is acting as both a resource server AND an identity provider

### Implementation Issues
1. **JWT Claim Processing**: Current implementation looks for `email` in token but spec requires `sub` to be the sole authoritative user identity
2. **Token Creation**: Multiple endpoints create tokens, violating the separation of concerns

## Recommendations

### Immediate Fixes Needed
1. Remove all token creation functionality from backend
2. Update JWT verification to use only `sub` claim for user identity (not `email`)
3. Remove BetterAuth-compatible endpoints that issue tokens
4. Update authentication logic to only verify externally issued tokens

### Files That Need Modification
1. `auth_service.py` - Remove token creation, fix JWT verification to use `sub` claim
2. `users.py` - Remove token issuing endpoints, keep only verification endpoints
3. `auth_middleware.py` - Ensure it only extracts identity from `sub` claim

## Compliance Status

### Current vs. Required
- ❌ **Current**: Backend issues tokens
- ✅ **Required**: Backend only verifies tokens

- ❌ **Current**: Backend uses email from token for identity
- ✅ **Required**: Backend uses only `sub` claim from token for identity

- ❌ **Current**: Backend has user registration/login endpoints that issue tokens
- ✅ **Required**: Backend only verifies tokens from BetterAuth

## Summary
The current backend structure has critical authentication boundary violations. The backend is currently operating as both a resource server AND an identity provider, which contradicts the specification. All token creation functionality must be removed to comply with the requirement that "Backend does NOT issue tokens, manage sessions, or replicate Better Auth".