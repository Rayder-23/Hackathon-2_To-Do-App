# Implementation Plan: 2.5-auth-alignment - Backend-Frontend Authentication Alignment

**Branch**: `2.5-auth-alignment` | **Date**: 2026-01-29 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/2.5-auth-alignment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan implements the alignment between Better Auth frontend and FastAPI backend to establish a proper authentication boundary. The backend becomes a stateless JWT-verifying resource server that derives user identity exclusively from verified JWT claims, while Better Auth handles all authentication flows in the frontend environment. This creates a clear separation of concerns where authentication is fully owned by Better Auth and the backend strictly enforces authorization based on verified tokens.

## 1. Architecture Sketch

### Authentication Ownership Boundaries
```
┌─────────────────┐                ┌──────────────────┐
│   Frontend      │                │    Backend       │
│  (Next.js +    │                │   (FastAPI)      │
│  Better Auth)   │                │                  │
├─────────────────┤                ├──────────────────┤
│ • User signup   │◄──JWT Token──►│ • JWT Validation │
│ • User signin   │                │ • Identity Deriv.│
│ • Session mgmt  │                │ • Authorization  │
│ • JWT issuance  │                │ • Resource Access│
│ • UI rendering  │                │ • Task ownership │
└─────────────────┘                └──────────────────┘
```

### JWT Flow from Frontend to Backend
1. User authenticates via Better Auth in frontend
2. Better Auth issues JWT with shared secret
3. Frontend attaches JWT to Authorization header
4. Backend verifies JWT signature using BETTER_AUTH_SECRET
5. Backend extracts user identity from `sub` claim
6. Backend enforces authorization based on verified identity

### Backend Role as Stateless Resource Server
- No session state maintained
- No token issuance or refresh
- No user credential storage
- Pure JWT validation and resource access control
- Database-level ownership filtering

## 2. End-to-End Request Flow (Concrete)

### Step 1: User Authentication in Better Auth
1. User enters credentials in Next.js frontend
2. Better Auth processes authentication request
3. Better Auth generates JWT with claims: `sub`, `exp`, `iat`
4. JWT is signed with BETTER_AUTH_SECRET

### Step 2: JWT Issuance in Frontend Environment
1. Better Auth stores JWT in browser session
2. Frontend can retrieve JWT using authClient.token()
3. JWT contains canonical user ID in `sub` claim

### Step 3: API Request with Authorization Header
1. Frontend makes API call to backend
2. Frontend adds header: `Authorization: Bearer <JWT>`
3. Request sent to backend endpoint (e.g., `/api/users/{user_id}/tasks`)

### Step 4: Backend Verification and Authorization Steps
1. Backend receives request with Authorization header
2. Extract JWT from Authorization header
3. Verify JWT signature using BETTER_AUTH_SECRET
4. Validate expiration with 5-second clock skew tolerance
5. Verify required claims (`sub`, `exp`, `iat`) exist
6. Compare JWT `sub` claim with URL `{user_id}`
7. If match, proceed with request; if mismatch, return 403
8. Apply database-level filtering for user-owned resources

## 3. Backend Behavior (Step-by-Step, Technical)

### Step 1: JWT Extraction
- Extract JWT from `Authorization: Bearer <token>` header
- Return 401 if no Authorization header present
- Return 401 if header format is incorrect

### Step 2: Signature Verification using BETTER_AUTH_SECRET
- Use HMAC-SHA256 to verify JWT signature
- Load secret from environment variable `BETTER_AUTH_SECRET`
- Return 401 if signature verification fails

### Step 3: Claim Validation (exp, sub, etc.)
- Validate `exp` claim against current time with 5-second tolerance
- Validate `iat` claim exists and is reasonable
- Validate `sub` claim exists and contains canonical user ID
- Return 401 if any required claims missing or invalid

### Step 4: Identity Derivation
- Extract user identity from `sub` claim
- Treat this as the sole authoritative user identity
- Do not accept user ID from URL, body, or other sources

### Step 5: URL vs JWT Identity Enforcement
- Extract `{user_id}` from request URL path
- Compare with JWT `sub` claim
- Return 403 if these do not match
- Proceed only if they match exactly

### Step 6: Database-Level Ownership Filtering
- Query database with user ID derived from JWT `sub`
- Ensure all queries are scoped to authenticated user
- Never return data belonging to other users
- Apply ownership filters to all SELECT, UPDATE, DELETE operations

## 4. Explicit Non-Responsibilities

### What the Backend Must Never Do
- Issue, refresh, or manage JWT tokens
- Handle user signup, signin, or password reset flows
- Store or manage session state
- Process authentication credentials directly
- Call Better Auth APIs for authentication purposes
- Accept user identity from sources other than verified JWT claims

### Which Auth Concepts Are Frontend-Only
- User credential validation
- Password hashing and storage
- Session management
- Account creation and verification
- Password reset workflows
- Social login providers

### What Logic Must Be Deleted or Avoided
- Any token issuance or refresh endpoints
- Session-based authentication logic
- Direct credential validation in backend
- Cookie-based authentication
- User registration endpoints
- Password change endpoints
- Any authentication state storage in backend

## 5. Decisions Needing Documentation

### Required JWT Claims and Their Meaning
- `sub`: Canonical user ID (string) - used for identity derivation
- `exp`: Expiration timestamp (number) - used for validation
- `iat`: Issued-at timestamp (number) - used for validation
- Optional: `email`, `name`, `iss`, `aud` - for additional context

### Error Code Semantics (401 vs 403)
- 401 Unauthorized: Invalid/missing JWT, signature failure, expired token
- 403 Forbidden: Valid JWT but insufficient permissions (user ID mismatch)

### Endpoint Behavior Guarantees
- All endpoints require valid JWT in Authorization header
- All user-scoped endpoints enforce JWT `sub` vs URL `{user_id}` match
- All database queries are filtered by authenticated user ID
- All error responses include descriptive messages without sensitive information

### Security Tradeoffs (Shared Secret vs JWKS)
- Shared secret (HMAC): Simpler implementation, symmetric signing
- JWKS: More scalable, supports multiple keys, asymmetric algorithms
- Decision: Use shared secret for simplicity and consistency with Better Auth

## 6. Validation Strategy

### How to Verify Backend Rejects Unauthenticated Requests
- Send requests without Authorization header → expect 401
- Send requests with malformed Authorization header → expect 401
- Send requests with invalid JWT → expect 401
- Send requests with expired JWT → expect 401

### How to Verify Cross-User Access Is Impossible
- Authenticate as User A, get JWT
- Request data for User B with User A's JWT → expect 403
- Attempt to modify User B's data with User A's JWT → expect 403
- Verify all responses only contain User A's data

### How to Detect Accidental Authentication Bypass
- Monitor logs for requests without proper JWT validation
- Implement audit trail for all authorization decisions
- Track requests where URL user_id != JWT sub claim
- Set up alerts for unusual access patterns or privilege escalation attempts

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript (frontend)
**Primary Dependencies**: FastAPI (backend), Better Auth (frontend), SQLModel, Neon PostgreSQL
**Storage**: Neon Serverless PostgreSQL database
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web application (Linux server + browser)
**Project Type**: Web (frontend + backend)
**Performance Goals**: JWT signature verification completes within 100ms for 95% of requests
**Constraints**: <200ms p95 for API requests, JWT validation with 5-second clock skew tolerance, zero-trust authentication model
**Scale/Scope**: Multi-user system with proper authentication and authorization boundaries

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Authentication and Authorization Compliance
- ✅ Better Auth runs in TypeScript frontend environment (Constitution line 82)
- ✅ JWT tokens are the sole mechanism for identity transfer (Constitution line 84)
- ✅ JWT tokens are signed using shared secret (Constitution line 85)
- ✅ Shared secret provided via BETTER_AUTH_SECRET environment variable (Constitution line 86)
- ✅ Both frontend and backend load same BETTER_AUTH_SECRET (Constitution line 87)
- ✅ Every API request includes Authorization: Bearer <JWT> (Constitution line 89-90)
- ✅ Backend verifies JWT signature using BETTER_AUTH_SECRET (Constitution line 93)
- ✅ Backend verifies JWT expiry and standard claims (Constitution line 94)
- ✅ Backend treats verified JWT claims as authoritative identity (Constitution line 95)
- ✅ Requests without valid JWT receive 401 Unauthorized (Constitution line 97)
- ✅ Cross-user access requests receive 403 Forbidden (Constitution line 99)

### Separation of Concerns Compliance
- ✅ Frontend handles user signup and signin (Constitution line 66)
- ✅ Frontend handles session handling and JWT issuance (Constitution line 67)
- ✅ Backend only verifies JWT tokens on every request (Constitution line 76)
- ✅ Backend enforces task ownership on all operations (Constitution line 78)
- ✅ Clear separation between frontend and backend responsibilities (Constitution line 24)

### Zero-Trust Architecture Compliance
- ✅ Backend never trusts client-provided identity (Constitution line 109)
- ✅ Backend derives user identity exclusively from verified JWT claims (Constitution line 110)
- ✅ Backend rejects requests where URL user_id doesn't match JWT identity (Constitution line 96)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   └── user.py
│   ├── services/
│   │   ├── user_service.py
│   │   └── auth_service.py
│   ├── api/
│   │   └── routes/
│   │       └── users.py
│   ├── dependencies/
│   │   └── auth.py
│   └── main.py
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   │   └── auth-service.ts
│   └── lib/
│       └── better-auth-client.ts
└── tests/
```

**Structure Decision**: Selected web application structure with separate frontend and backend. Backend contains authentication middleware and user management services. Frontend contains Better Auth integration and JWT token handling services. This structure maintains clear separation of concerns between authentication (frontend) and authorization (backend).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
