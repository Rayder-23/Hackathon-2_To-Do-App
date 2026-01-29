# Tasks: 2.5-auth-alignment - Backend-Frontend Authentication Alignment

## Task 1: Documentation Grounding (Better Auth + JWT Model)
**Objective**: Establish authoritative documentation for Better Auth JWT implementation and JWT validation patterns
**Inputs**: Better Auth documentation, JWT RFC standards, Context7 library docs
**Outputs**: Grounded documentation summary, JWT claim structure specification, authentication flow patterns
**Validation**: All implementation decisions are MCP-grounded, no undocumented features used
**Dependencies**: None
**Category**: Research

## Task 2: Backend Auth Boundary Audit
**Objective**: Identify all current backend authentication assumptions and behaviors that conflict with spec
**Inputs**: Current backend codebase, feature spec, auth alignment requirements
**Outputs**: Audit report of incorrect auth assumptions, list of endpoints requiring changes
**Validation**: Complete mapping of current vs required auth behavior
**Dependencies**: Task 1
**Category**: Analysis

## Task 3: Remove/Deprecate Invalid Backend Auth Behavior
**Objective**: Eliminate any backend authentication logic that violates the spec
**Inputs**: Audit report from Task 2, current backend implementation
**Outputs**: Cleaned backend code without invalid auth logic, updated imports/removals
**Validation**: No remaining backend auth flows that should be frontend-only
**Dependencies**: Task 2
**Category**: Cleanup

## Task 4: JWT Verification Middleware Design
**Objective**: Design and implement JWT verification middleware for FastAPI
**Inputs**: JWT documentation from Task 1, security requirements, FastAPI patterns
**Outputs**: JWT verification service, authentication dependency, middleware implementation
**Validation**: Middleware correctly validates JWT signature, expiration, and required claims
**Dependencies**: Task 1
**Category**: Implementation

## Task 5: Identity Derivation and Authorization Rules
**Objective**: Implement logic to derive user identity from JWT and enforce authorization
**Inputs**: JWT middleware from Task 4, authorization requirements, user data model
**Outputs**: Identity derivation service, authorization enforcement logic, user context
**Validation**: User identity derived exclusively from JWT `sub` claim, proper authorization checks
**Dependencies**: Task 4
**Category**: Implementation

## Task 6: Endpoint Behavior Alignment
**Objective**: Update all endpoints to enforce JWT-based authentication and authorization
**Inputs**: Current endpoints, auth requirements, middleware from Task 4
**Outputs**: Updated endpoint decorators, authentication enforcement on all routes
**Validation**: All endpoints reject requests without valid JWT, enforce user ownership
**Dependencies**: Task 4, Task 5
**Category**: Implementation

## Task 7: Error Handling and Status Code Validation
**Objective**: Implement proper error responses with correct HTTP status codes
**Inputs**: Error handling requirements, spec-defined status codes (401 vs 403)
**Outputs**: Standardized error responses, proper 401/403 handling, descriptive error messages
**Validation**: 401 for auth failures, 403 for authorization failures, no information leakage
**Dependencies**: Task 6
**Category**: Implementation

## Task 8: Security Review and Regression Checks
**Objective**: Verify all security requirements are met and no regressions introduced
**Inputs**: Completed implementation, security requirements, penetration testing scenarios
**Outputs**: Security validation report, test results confirming compliance
**Validation**: All auth requirements satisfied, no cross-user access possible, proper logging
**Dependencies**: Task 7
**Category**: Validation