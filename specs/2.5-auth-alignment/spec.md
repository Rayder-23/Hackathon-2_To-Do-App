# Feature Specification: 1-auth-alignment: Backend–Frontend Authentication Alignment

**Feature Branch**: `2.5-auth-alignment`
**Created**: 2026-01-29
**Status**: Draft
**Input**: User description: "Mini Phase 2.5: Backend–Frontend Authentication Alignment

Target audience:
- Developers aligning a FastAPI backend with a Next.js 16 + Better Auth frontend
- Reviewers validating JWT-based authentication and authorization boundaries

Objective:
Align the FastAPI backend with a Better Auth–based frontend so that:
- Authentication is fully owned by Better Auth (TypeScript / Next.js)
- The backend acts strictly as a JWT-verifying resource server
- All identity and authorization decisions are derived from verified JWT claims

Architectural decision (Solution A):
- Better Auth runs exclusively in the TypeScript / Next.js environment
- Better Auth handles signup, signin, sessions, and JWT issuance
- FastAPI does not issue, refresh, or manage tokens or sessions
- FastAPI only verifies incoming JWTs and enforces authorization

JWT Claims Contract (Authoritative):
- Required claims:
  - `sub` (string): canonical user ID
  - `exp` (number): expiration timestamp
  - `iat` (number): issued-at timestamp
- Optional claims:
  - `email`, `name`, `iss`, `aud`
- `sub` is the sole authoritative user identity
- Backend must reject tokens missing required claims
- Backend must reject requests where `{user_id}` does not match `sub`
- JWTs are signed using HMAC with the shared secret `BETTER_AUTH_SECRET`
- Backend must verify signature and expiry before trusting any claim

Scope:
- Modify backend authentication middleware and request handling
- Enforce JWT verification and authorization consistently
- Remove any backend behavior that attempts to emulate Better Auth

Out of scope:
- Authentication flows in FastAPI
- Session or cookie handling in the backend
- Token issuance or refresh logic
- Replicating Better Auth endpoints
- Token issuance (handled by Better Auth frontend)
- Session management (handled by Better Auth frontend)
- Password management (handled by Better Auth frontend)
- User registration workflow (handled by Better Auth frontend)

Success criteria:
- Backend accepts requests only with valid JWTs
- Backend derives user identity exclusively from JWT `sub`
- Backend enforces strict task ownership
- Backend behavior matches the documented end-to-end JWT flow
- No ambiguity exists regarding auth responsibilities

Constraints:
- JWTs are signed using `BETTER_AUTH_SECRET`
- Backend must not call Better Auth APIs
- Backend must not issue tokens
- JWT expiration validation allows 5-second clock skew tolerance
- Authentication failure events must be logged for security monitoring
- Backend must return descriptive error messages for invalid JWT tokens
- Shared secret `BETTER_AUTH_SECRET` must be managed through secure configuration (environment variables/secrets manager)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticate API requests with JWT tokens (Priority: P1)

A user signs in through the Next.js frontend using Better Auth, then makes API requests to the FastAPI backend. The backend validates the JWT token provided by Better Auth and allows access to protected resources based on the token's claims.

**Why this priority**: This is the core functionality that enables the entire authentication flow - without this, no backend resources can be accessed securely.

**Independent Test**: Can be fully tested by making an API call with a valid JWT token from Better Auth and verifying access is granted, while calls without tokens or with invalid tokens are rejected.

**Acceptance Scenarios**:

1. **Given** a user has authenticated with Better Auth and received a valid JWT token, **When** the user makes an API request with the token in the Authorization header, **Then** the backend verifies the token and grants access to the requested resource
2. **Given** a user makes an API request without a JWT token, **When** the request reaches the backend, **Then** the backend rejects the request with a 401 Unauthorized response

---

### User Story 2 - Enforce strict task ownership based on JWT claims (Priority: P2)

A user accesses their personal tasks through the API, and the backend ensures they can only access tasks belonging to their user ID as specified in the JWT `sub` claim.

**Why this priority**: Critical for data security and privacy - users must not be able to access other users' data.

**Independent Test**: Can be tested by having a user attempt to access their own tasks (should succeed) versus accessing another user's tasks (should fail).

**Acceptance Scenarios**:

1. **Given** a user makes a request to access their own tasks with a valid JWT containing their user ID in the `sub` claim, **When** the backend verifies the token and compares the `sub` claim with the requested user ID, **Then** the backend grants access to the tasks
2. **Given** a user makes a request to access another user's tasks with a valid JWT containing a different user ID in the `sub` claim, **When** the backend verifies the token and compares the `sub` claim with the requested user ID, **Then** the backend rejects the request with a 403 Forbidden response

---

### User Story 3 - Validate JWT token integrity and expiration (Priority: P3)

The backend verifies that incoming JWT tokens are properly signed with the shared secret and have not expired before granting access to resources.

**Why this priority**: Essential for security - prevents token forgery and ensures access is time-limited as intended.

**Independent Test**: Can be tested by sending requests with valid tokens (should succeed), expired tokens (should fail), and forged tokens (should fail).

**Acceptance Scenarios**:

1. **Given** a user makes a request with a valid, unexpired JWT token signed with the correct secret, **When** the backend verifies the token signature and expiration, **Then** the backend grants access to the requested resource
2. **Given** a user makes a request with an expired JWT token, **When** the backend verifies the token expiration, **Then** the backend rejects the request with a 401 Unauthorized response
3. **Given** a user makes a request with a JWT token missing required claims (`sub`, `exp`, `iat`), **When** the backend validates the token claims, **Then** the backend rejects the request with a 401 Unauthorized response and descriptive error message
4. **Given** a user makes a request with a JWT token that has an invalid signature, **When** the backend verifies the token signature, **Then** the backend rejects the request with a 401 Unauthorized response

---

### Edge Cases

- **EC-001**: What happens when a JWT token is missing required claims (`sub`, `exp`, `iat`)? → System returns 401 Unauthorized with descriptive error message
- **EC-002**: How does the system handle JWT tokens with invalid signatures? → System returns 401 Unauthorized with generic error to prevent signature verification timing attacks
- **EC-003**: What occurs when the `sub` claim doesn't match the expected user ID format? → System returns 401 Unauthorized with descriptive error message
- **EC-004**: What happens when JWT token has expired (with 5-second tolerance)? → System returns 401 Unauthorized with instruction to refresh token at frontend
- **EC-005**: What occurs when `{user_id}` in URL doesn't match JWT `sub` claim? → System returns 403 Forbidden with clear access denied message
- **EC-006**: How does the system handle malformed Authorization header? → System returns 401 Unauthorized with descriptive error message

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify incoming JWT tokens using the shared `BETTER_AUTH_SECRET`
- **FR-002**: System MUST reject requests with JWT tokens missing required claims (`sub`, `exp`, `iat`)
- **FR-003**: System MUST derive user identity exclusively from the JWT `sub` claim
- **FR-004**: System MUST enforce that `{user_id}` in URL path matches the `sub` claim in JWT token
- **FR-005**: System MUST validate JWT token expiration before granting access
- **FR-006**: System MUST verify JWT token signature integrity using HMAC with shared secret
- **FR-007**: System MUST reject requests without valid Authorization header containing Bearer token
- **FR-008**: System MUST log authentication failures for security monitoring with appropriate severity levels
- **FR-009**: System MUST accept JWT tokens with up to 5-second clock skew tolerance for expiration validation
- **FR-010**: System MUST return 403 Forbidden when `{user_id}` in URL path does not match JWT `sub` claim
- **FR-011**: System MUST follow this request handling flow: Receive request → Extract JWT from Authorization header → Validate JWT according to NFR-004 → Extract `sub` claim → Compare with URL/user context → Process or reject request
- **FR-012**: System MUST return 401 Unauthorized for invalid/missing JWT, and 403 Forbidden for valid JWT but insufficient permissions
- **FR-013**: System MUST ignore cookies completely and rely only on Authorization header for authentication

### Non-functional Requirements

- **NFR-001**: JWT signature verification MUST complete within 100ms for 95% of requests as measured in production-like environment
- **NFR-002**: System MUST handle missing required JWT claims by returning 401 Unauthorized with descriptive error message
- **NFR-003**: System MUST implement rate limiting for authentication failure attempts to prevent brute force attacks
- **NFR-004**: JWT validation MUST follow this sequence: signature verification → expiration → required claims → sub claim match

### Key Entities *(include if feature involves data)*

- **JWT Token**: Authentication credential containing user identity and authorization claims, signed with shared secret
- **User Identity**: Represented by the `sub` claim in JWT token, used for access control decisions
- **Authentication Log**: Record of authentication attempts, successes, and failures for security monitoring

## Clarifications

### Session 2026-01-29

- Q: When validating JWT tokens, in what order should the backend perform these checks? → A: Signature verification → Expiration → Required claims → Sub claim match
- Q: What should be the explicit step-by-step request handling flow for the backend when processing authenticated requests? → A: Receive request → Extract JWT from Authorization header → Validate JWT according to NFR-004 → Extract `sub` claim → Compare with URL/user context → Process or reject request
- Q: What HTTP status codes should be used for different types of authentication/authorization failures? → A: 401 for invalid/missing JWT, 403 for valid JWT but insufficient permissions
- Q: Should the backend consider cookies when processing authentication, or should it rely solely on the Authorization header? → A: Backend should ignore cookies completely, relying only on Authorization header
- Q: Which of the following should be explicitly listed as backend non-responsibilities to ensure proper separation of concerns? → A: Token issuance, session management, password management, user registration workflow

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of API requests with valid JWT tokens are accepted and processed successfully
- **SC-002**: 100% of API requests without valid JWT tokens are rejected with appropriate error responses
- **SC-003**: 100% of requests where `{user_id}` does not match JWT `sub` claim are rejected with 403 Forbidden
- **SC-004**: All JWT tokens with expired timestamps (including 5-second clock skew tolerance) are rejected with 401 Unauthorized response
- **SC-005**: JWT signature verification completes within 100ms for 95% of requests as measured in production-like environment with representative load
- **SC-006**: 100% of authentication failure events are logged with appropriate severity for security monitoring
- **SC-007**: 100% of requests with JWT tokens missing required claims are rejected with 401 Unauthorized response and descriptive error message