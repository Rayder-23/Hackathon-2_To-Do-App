# Research Summary: Todo Application Phase II Implementation

## JWT Claim Structure and Validation Rules

**Decision**: Use standard JWT claims (sub, email, exp, iat) with Better Auth for token generation and FastAPI for verification

**Rationale**: This follows industry standards and ensures consistency between frontend token generation and backend validation. The sub claim serves as user ID, email for identity verification, exp for expiration, and iat for issued-at timestamp.

**Alternatives considered**:
- Custom claims structure (rejected for non-standard approach)
- Different token formats (rejected for complexity and security concerns)

## API URL Structure and Consistency

**Decision**: Implement RESTful API with consistent URL patterns: `/api/{user_id}/tasks` for user-specific operations

**Rationale**: This provides clear resource organization and follows REST conventions. The user_id in the URL allows for clear scoping while the backend verifies this matches the authenticated user's identity.

**Alternatives considered**:
- `/api/tasks/{user_id}` (rejected for less intuitive resource hierarchy)
- Query parameters instead of path variables (rejected for not following REST conventions)

## Database Schema Tradeoffs

**Decision**: Use SQLModel with PostgreSQL for data persistence with foreign key relationships between User and Task entities

**Rationale**: SQLModel provides type safety with Python typing, integrates well with FastAPI, and supports both SQLAlchemy and Pydantic features. PostgreSQL offers robust ACID compliance and scalability.

**Alternatives considered**:
- Pure SQLAlchemy (rejected for losing Pydantic integration benefits)
- Alternative ORMs (rejected for ecosystem compatibility with FastAPI)

## Auth Failure Handling Strategies

**Decision**: Return RFC 7807 Problem Details format for all auth failures with specific HTTP status codes

**Rationale**: This provides structured error information that's easy for clients to parse and follows established standards for API error responses.

**Alternatives considered**:
- Custom error formats (rejected for lack of standardization)
- Generic error responses (rejected for insufficient debugging information)

## Frontend Session Storage Strategy

**Decision**: Store JWT tokens in browser's httpOnly cookies managed by Better Auth

**Rationale**: httpOnly cookies protect against XSS attacks and are automatically sent with requests. Better Auth handles the complexity of secure token storage and management.

**Alternatives considered**:
- Local storage (rejected for XSS vulnerability)
- Session storage (rejected for same XSS vulnerability and shorter persistence)