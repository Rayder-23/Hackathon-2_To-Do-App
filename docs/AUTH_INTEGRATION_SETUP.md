# BetterAuth Integration Setup

This document explains how to properly set up BetterAuth with the Todo App frontend and backend.

## Architecture Overview

The authentication flow is designed as follows:

1. **Frontend (Next.js)**: Contains BetterAuth client and server-side configuration
2. **Backend (FastAPI)**: Acts as a JWT-verifying resource server, only validating tokens issued by BetterAuth
3. **Authentication Flow**: 
   - User registers/logs in via BetterAuth on the frontend
   - BetterAuth issues JWT tokens
   - Frontend attaches JWT to requests to backend
   - Backend verifies JWT using shared secret

## Setup Instructions

### 1. Frontend Setup

The frontend contains:

- `src/lib/auth.ts` - BetterAuth server-side configuration
- `src/app/api/auth/[...betterAuth]/route.ts` - BetterAuth API route handler
- `src/services/auth-service.ts` - BetterAuth client integration
- `.env.local` - Environment variables

### 2. Backend Setup

The backend contains:

- `src/config.py` - Configuration for JWT verification using shared secret
- `src/services/auth_service.py` - JWT verification logic
- `src/api/middleware/auth_middleware.py` - Authentication middleware
- `.env` - Environment variables

### 3. Environment Variables

Both frontend and backend must use the SAME `BETTER_AUTH_SECRET` value:

Frontend (.env.local):
```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-jwt-signing-key-here-make-it-long-and-random
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
DATABASE_URL=file:./db.sqlite
```

Backend (.env):
```
BETTER_AUTH_SECRET=your-super-secret-jwt-signing-key-here-make-it-long-and-random
```

## Running the Application

1. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

2. Start the backend:
   ```bash
   cd backend
   uv run python -m src.main
   ```

## Troubleshooting

### Common Issues

1. **"Failed to get authentication token" Error**
   - Check that both frontend and backend have the same `BETTER_AUTH_SECRET`
   - Verify that the frontend's `NEXT_PUBLIC_BETTER_AUTH_URL` matches where BetterAuth is running
   - Ensure the backend's API URL matches what the frontend is calling

2. **401 Unauthorized Errors**
   - Verify JWT tokens are being properly attached to requests
   - Check that the token hasn't expired
   - Confirm the token contains the required claims (`sub`, `exp`, `iat`)

3. **User ID Mismatch (403 Forbidden)**
   - The JWT `sub` claim must match the user ID in the URL path
   - Example: If JWT `sub` is "123", the URL should be `/api/123/tasks`