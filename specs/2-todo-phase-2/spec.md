# Feature Specification: Todo Application – Phase II: Full-Stack Web System

**Feature Branch**: `2-todo-phase-2`
**Created**: 2026-01-11
**Status**: Draft
**Input**: User description: "Todo Application – Phase II: Full-Stack Web System

Target audience:
- Developers implementing a secure, multi-user web application
- Reviewers evaluating spec-driven architecture and authentication design

Objective:
Transform the Phase I in-memory console todo application into a full-stack,
multi-user web application with persistent storage and authentication.

Scope:
- Implement all five basic task features (add, list, update, delete, toggle complete)
- Introduce user authentication and per-user task isolation
- Persist data using a relational database
- Expose functionality via a RESTful API
- Provide a responsive web-based frontend UI

Technology stack:
Frontend:
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (TypeScript-based)
Backend:
- Python FastAPI
- SQLModel ORM
- Neon Serverless PostgreSQL
Auth:
- JWT-based authentication using Better Auth-issued tokens
Spec-driven development:
- Claude Code
- Spec-Kit Plus
- MCP documentation grounding via the "mcp-doc-grounding" skill

Success criteria:
- Users can sign up and sign in
- Authenticated users receive JWT tokens
- All API requests require valid JWT tokens
- Users can only access and modify their own tasks
- All five task operations work end-to-end via the web UI
- Backend rejects unauthorized and cross-user access
- Frontend and backend behavior matches the written specification

Constraints:
- All frontend code resides in the `frontend` directory
- All backend Python source code resides in `backend/src`
- Authentication is enforced server-side on every request
- JWT verification is mandatory for all API endpoints
- External documentation must be sourced via MCP only

Not building:
- Role-based access control
- Task sharing between users
- Realtime updates (WebSockets)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Authentication (Priority: P1)

As a new user, I want to create an account so that I can securely access my personal todo list.

**Why this priority**: This is the foundational capability that enables all other functionality. Without user registration and authentication, users cannot have isolated todo lists.

**Independent Test**: Can be fully tested by registering a new user account, verifying the account creation process, and confirming that the user receives proper authentication tokens upon successful registration.

**Acceptance Scenarios**:

1. **Given** I am a new visitor to the application, **When** I complete the registration form with valid information and submit it, **Then** my account is created and I am logged in with appropriate authentication tokens.

2. **Given** I am an existing user with an account, **When** I enter my credentials on the login page and submit, **Then** I am authenticated and granted access to my todo list with valid JWT tokens.

---

### User Story 2 - Personal Todo Management (Priority: P1)

As an authenticated user, I want to manage my personal todo list (add, list, update, delete, toggle complete) so that I can organize my tasks effectively.

**Why this priority**: This represents the core functionality of the todo application that provides value to users. It's the primary reason users would engage with the application.

**Independent Test**: Can be fully tested by logging in as an authenticated user and performing all five basic task operations (add, list, update, delete, toggle complete) on my personal todo list.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user on the todo list page, **When** I enter a new task and save it, **Then** the task appears in my personal todo list.

2. **Given** I have tasks in my todo list, **When** I view the list, **Then** I see all my tasks organized in the expected manner.

3. **Given** I have a task in my todo list, **When** I update its details, **Then** the changes are saved and reflected in my list.

4. **Given** I have a task in my todo list, **When** I delete it, **Then** the task is removed from my list.

5. **Given** I have an incomplete task in my todo list, **When** I toggle its completion status, **Then** the task status is updated to reflect its new state.

---

### User Story 3 - Secure Access Control (Priority: P2)

As an authenticated user, I want to ensure that I can only access my own tasks so that my personal information remains private and secure.

**Why this priority**: This is critical for maintaining user trust and ensuring data privacy. Without proper access controls, users' data could be exposed to other users.

**Independent Test**: Can be fully tested by creating multiple user accounts, having each user create tasks, and verifying that users can only access their own tasks and cannot view or modify others' tasks.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user, **When** I attempt to access another user's tasks through direct API calls or URL manipulation, **Then** the request is denied with appropriate authorization error.

2. **Given** I am an unauthenticated user, **When** I attempt to access any todo functionality, **Then** I am redirected to the login page or receive an authentication error.

---

### Edge Cases

- What happens when a user attempts to access tasks with invalid/expired JWT tokens? (System returns HTTP 401 Unauthorized)
- How does the system handle database connection failures during task operations? (System returns HTTP 503 Service Unavailable with retry recommendation)
- What occurs when a user tries to create a task while offline or with poor connectivity? (UI shows appropriate error message and allows retry)
- How does the system behave when a user attempts to register with an already-used email address? (System returns HTTP 409 Conflict)
- What happens when a user attempts to access another user's tasks? (System returns HTTP 403 Forbidden)
- How does the system handle rate limiting when exceeding 100 requests per hour? (System returns HTTP 429 Too Many Requests)
- What occurs when a user enters input that fails validation? (System returns HTTP 400 Bad Request with specific error details)
- How does the system handle attempts to modify a task that doesn't belong to the user? (System returns HTTP 403 Forbidden)
- What happens when a request has no JWT token? (System returns HTTP 401 Unauthorized)
- How does the system handle tampered JWT tokens? (System returns HTTP 401 Unauthorized)
- What occurs when a user tries to access a task with mismatched user_id in URL? (System returns HTTP 403 Forbidden)
- How does the system handle requests without proper Authorization header? (System returns HTTP 401 Unauthorized)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to register with email and password credentials
- **FR-002**: System MUST authenticate users via JWT tokens issued by Better Auth with expiration after 24 hours and refresh tokens valid for 7 days
- **FR-003**: Users MUST be able to add new tasks to their personal todo list with titles up to 255 characters and descriptions up to 1000 characters
- **FR-003.1**: System MUST return HTTP 400 Bad Request when task title exceeds 255 characters
- **FR-003.2**: System MUST return HTTP 400 Bad Request when task description exceeds 1000 characters
- **FR-004**: Users MUST be able to view their complete todo list sorted by creation date (most recent first)
- **FR-005**: Users MUST be able to update details of their existing tasks including title, description, and completion status
- **FR-006**: Users MUST be able to delete their own tasks, with soft deletion (marked as deleted but retained for 30 days)
- **FR-006.1**: Soft-deleted tasks MUST NOT appear in normal task list queries
- **FR-006.2**: Soft-deleted tasks MUST be accessible via special endpoint with explicit permission
- **FR-007**: Users MUST be able to toggle the completion status of their tasks
- **FR-008**: System MUST persist all task data in a PostgreSQL database with proper foreign key relationships between users and tasks
- **FR-009**: System MUST enforce authentication for all API endpoints with valid JWT tokens
- **FR-010**: System MUST ensure users can only access their own tasks and MUST return appropriate HTTP 403 Forbidden errors when unauthorized access is attempted
- **FR-011**: System MUST provide a responsive web UI that supports screen sizes from 320px to 1920px with mobile-first design
- **FR-012**: System MUST validate all user inputs using OWASP ASVS standards to prevent injection attacks
- **FR-013**: System MUST reject user registration attempts with duplicate email addresses and return HTTP 409 Conflict
- **FR-014**: System MUST validate email format using the pattern /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
- **FR-015**: System MUST implement rate limiting of 100 requests per hour per IP address AND 500 requests per hour per authenticated user to prevent abuse
- **FR-016**: System MUST validate JWT tokens contain required claims: sub (user ID), email, exp, iat
- **FR-016.1**: System MUST return HTTP 401 Unauthorized for JWT tokens missing required claims
- **FR-016.2**: System MUST return HTTP 401 Unauthorized for JWT tokens with malformed claims
- **FR-017**: System MUST return RFC 7807 Problem Details format for all auth failures: {status, title, detail}
- **FR-018**: System MUST return HTTP 404 for both deleted and nonexistent tasks to maintain security
- **FR-019**: System MUST configure Better Auth to issue JWT tokens using BETTER_AUTH_SECRET environment variable
- **FR-020**: System MUST verify JWT signature using BETTER_AUTH_SECRET on every API request
- **FR-021**: System MUST extract user identity exclusively from verified JWT claims (zero-trust approach)
- **FR-022**: System MUST reject requests where URL user_id does not match authenticated JWT user identity
- **FR-023**: System MUST filter all responses to include only data owned by authenticated user
- **FR-024**: System MUST return HTTP 401 Unauthorized for requests without valid JWT
- **FR-025**: System MUST return HTTP 401 Unauthorized for invalid, expired, or tampered JWTs
- **FR-026**: System MUST return HTTP 403 Forbidden for authenticated requests attempting cross-user access

### Key Entities

- **User**: Represents a registered user with authentication credentials, uniquely identified by email address (enforced as unique in the database)
- **Task**: Represents a todo item belonging to a specific user, with properties like title (max 255 chars, required), user_id (required), creation timestamp (required), description (max 1000 chars, optional), and completion status (optional). Tasks cannot change ownership after creation.
- **Authentication Token**: JWT token issued to authenticated users for accessing protected endpoints with 24-hour expiration and refresh capability

### Constraints

- User email addresses must be unique across the system
- Task titles are limited to 255 characters maximum
- Task descriptions are limited to 1000 characters maximum
- JWT tokens expire after 24 hours with refresh tokens valid for 7 days
- All API endpoints require valid authentication tokens
- Users can only access, modify, or delete their own tasks
- Tasks cannot change ownership after creation
- Passwords must meet complexity requirements (minimum 8 characters with uppercase, lowercase, number, and special character)
- Frontend responsibilities: UI rendering and JWT storage/sending
- Backend responsibilities: All authorization enforcement and validation
- Better Auth must be configured to issue JWT tokens with shared secret via BETTER_AUTH_SECRET environment variable
- JWT tokens must be signed using the shared secret and verified on every API request
- Every API request must include Authorization: Bearer <JWT> header
- Backend must verify JWT signature using BETTER_AUTH_SECRET and reject invalid/expired tokens
- Backend must derive user identity exclusively from verified JWT claims (zero-trust approach)
- Backend must reject requests where URL user_id does not match authenticated JWT user identity
- Backend must filter all responses to include only data owned by authenticated user

### API Endpoint Specifications

- **POST /api/users/register**: Register new user with email and password
- **POST /api/users/login**: Authenticate user and return JWT
- **GET /api/{user_id}/tasks**: Retrieve user's tasks (sorted by creation date)
- **POST /api/{user_id}/tasks**: Create new task for user
- **PUT /api/{user_id}/tasks/{task_id}**: Update specific task
- **DELETE /api/{user_id}/tasks/{task_id}**: Mark task as deleted (soft delete)
- **PATCH /api/{user_id}/tasks/{task_id}/toggle**: Toggle completion status
- **GET /api/{user_id}/tasks/deleted**: Retrieve soft-deleted tasks (admin endpoint)

### Non-Goals

- Password reset functionality (deferred to future release)
- Task sharing between users
- Role-based access control
- Realtime updates (WebSockets)
- Advanced search or filtering capabilities
- Export/import functionality

## Clarifications

### Session 2026-01-11

- Q: What fields are required vs optional for a task? → A: Required: title, user_id, creation timestamp; Optional: description, completion status
- Q: What JWT claims are required for authentication? → A: Required claims: sub (user ID), email, exp, iat
- Q: What are the frontend vs backend responsibilities for auth? → A: Frontend: UI, JWT storage/sending; Backend: All authZ enforcement
- Q: What format should error responses follow for auth failures? → A: RFC 7807 Problem Details format: {status, title, detail}
- Q: How should the system handle deleted or nonexistent tasks? → A: Return HTTP 404 for both deleted and nonexistent tasks

### Session 2026-01-11 (Refinement)

- Q: How should the system handle JWT tokens with missing or malformed claims? → A: Return HTTP 401 Unauthorized for both cases
- Q: What is the rate limiting approach (per user vs per IP)? → A: Dual approach - 100 requests/hr per IP AND 500 requests/hr per authenticated user
- Q: How should soft-deleted tasks be handled in API responses? → A: Soft-deleted tasks do not appear in normal queries but accessible via special endpoint
- Q: What validation behavior for input constraints? → A: Return HTTP 400 Bad Request when constraints are violated
- Q: What are the specific API endpoints? → A: Defined complete REST API contract with all endpoints and methods

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration in ≤60 seconds measured via analytics
- **SC-002**: Authenticated users can access their todo list within ≤2 seconds of page load as measured by browser performance monitoring
- **SC-003**: Users can perform all five basic task operations (add, list, update, delete, toggle) with ≥99% success rate over a 30-day period
- **SC-004**: System prevents unauthorized access to other users' tasks with 100% accuracy as validated by security testing
- **SC-005**: ≥95% of users successfully complete the registration and login process on first attempt as measured by conversion analytics
- **SC-006**: All API requests properly validate JWT authentication tokens with ≤100ms average validation time
- **SC-007**: System handles ≥1000 concurrent users without degradation in performance (response time ≤3 seconds)
- **SC-008**: Rate limiting functions correctly by blocking requests >100 per hour per IP with HTTP 429 response