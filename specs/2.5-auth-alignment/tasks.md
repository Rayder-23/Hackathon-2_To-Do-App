# Tasks: 2.5-auth-alignment - Backend-Frontend Authentication Alignment

## Phase 1: Setup
- [ ] T001 Create/update backend configuration files for JWT verification with Better Auth

## Phase 2: Foundational
- [X] T002 [P] Update existing auth_service.py in backend/src/services/auth_service.py to align with JWT-only verification
- [X] T003 [P] Update existing auth_middleware.py in backend/src/api/middleware/auth_middleware.py for Better Auth compatibility
- [X] T004 [P] Create JWT error handlers in backend/src/api/handlers/auth_errors.py

## Phase 3: [US1] Authenticate API requests with JWT tokens
- [X] T005 [US1] Update existing auth_service.py to enforce JWT-only validation from Better Auth
- [X] T006 [US1] Update auth dependency to extract user identity exclusively from JWT `sub` claim
- [X] T007 [US1] Configure JWT validation to check signature, expiration, and required claims
- [X] T008 [US1] Test valid JWT token acceptance in API requests
- [X] T009 [US1] Test invalid/missing JWT rejection with 401 Unauthorized response

## Phase 4: [US2] Enforce strict task ownership based on JWT claims
- [X] T010 [US2] Update auth_middleware.py to compare JWT `sub` claim with URL `user_id`
- [X] T011 [US2] Implement authorization logic to return 403 Forbidden for mismatched user access
- [X] T012 [US2] Test user accessing own tasks with matching JWT `sub` claim
- [X] T013 [US2] Test user attempting to access other user's tasks with 403 Forbidden response

## Phase 5: [US3] Validate JWT token integrity and expiration
- [X] T014 [US3] Implement JWT signature verification using BETTER_AUTH_SECRET
- [X] T015 [US3] Implement JWT expiration validation with 5-second clock skew tolerance
- [X] T016 [US3] Validate required JWT claims (`sub`, `exp`, `iat`) exist and are valid
- [X] T017 [US3] Test expired JWT token rejection with 401 Unauthorized response
- [X] T018 [US3] Test JWT token with invalid signature rejection with 401 Unauthorized response
- [X] T019 [US3] Test JWT token missing required claims rejection with 401 Unauthorized response

## Phase 6: Align backend behavior with frontend expectations
- [X] T020 [P] Remove/modify backend authentication endpoints that violate auth boundaries
- [X] T021 [P] Update API error responses to match frontend expectations
- [X] T022 [P] Configure proper Authorization header parsing for JWT tokens
- [X] T023 [P] Remove any cookie-based authentication logic from backend
- [X] T024 [P] Update logging to include authentication failure events for security monitoring

## Phase 7: Polish & Cross-Cutting Concerns
- [X] T025 [P] Update documentation for JWT-based authentication flow
- [X] T026 [P] Add security headers to authentication-related responses
- [X] T027 [P] Verify all endpoints properly validate JWT tokens before processing
- [X] T028 [P] Add performance tests to ensure JWT validation completes within 100ms p95
- [X] T029 [P] Conduct final security review of authentication implementation
- [X] T030 [P] Update environment configuration to use BETTER_AUTH_SECRET for JWT validation