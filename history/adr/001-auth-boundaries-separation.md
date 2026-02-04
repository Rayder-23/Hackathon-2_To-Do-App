# ADR 001: Authentication Boundaries Separation - Backend as JWT-Verifying Resource Server

## Status
Accepted

## Context
The system needs to integrate with BetterAuth for user authentication while maintaining clear separation of responsibilities. Previously, the backend was both verifying and issuing JWT tokens, creating a violation of the authentication boundary where the backend was replicating BetterAuth functionality.

## Decision
The backend will act as a JWT-verifying resource server that:
- Only validates JWT tokens issued by BetterAuth
- Derives user identity exclusively from the JWT 'sub' claim
- Does not issue, create, or manage any authentication tokens
- Enforces authorization by comparing JWT 'sub' claim with URL/user identifiers
- Returns appropriate HTTP status codes (401 for invalid JWT, 403 for valid JWT but insufficient permissions)

## Rationale
- Maintains clear separation of authentication (BetterAuth) vs authorization (backend) concerns
- Prevents token replication and potential security inconsistencies
- Aligns with industry best practices for microservice authentication
- Enables consistent user identity derivation using the authoritative 'sub' claim
- Provides proper error handling with distinct status codes for different failure types

## Implications
- Backend endpoints must validate JWT tokens before processing requests
- All user identity information comes from verified JWT claims, not database lookups for authentication
- Authorization logic compares JWT 'sub' with requested resource identifiers
- Error responses must differentiate between authentication (401) and authorization (403) failures
- Configuration requires shared secret (BETTER_AUTH_SECRET) from BetterAuth

## Alternatives Considered
- **Alternative 1**: Backend continues issuing its own tokens alongside BetterAuth
  - Rejected: Creates inconsistent authentication flows and violates separation of concerns
- **Alternative 2**: Backend handles all authentication but forwards to BetterAuth
  - Rejected: Still violates the principle that BetterAuth should be the sole authority

## Resulting Context
The backend now operates purely as a resource server with clear trust boundaries. User identity is exclusively derived from BetterAuth-issued JWTs, ensuring consistent authentication across the system while enabling the backend to enforce authorization policies based on verified identity claims.