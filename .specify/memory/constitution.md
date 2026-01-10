<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0 (major update to include full-stack web application)
- List of modified principles: Spec-driven Implementation → Spec-first development (expanded), Deterministic Logic (retained), Simplicity and Clarity (retained), Separation of Concerns (expanded), Forward Compatibility (expanded), Error Handling and User Experience (expanded)
- Added sections: Security by Design, Authentication and Authorization, API Contract Standards, MCP Documentation Grounding
- Removed sections: None
- Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md
- Follow-up TODOs: RATIFICATION_DATE needs to be set
-->
# Todo Application – Spec-Driven Backend + Full-Stack Web System Constitution

## Core Principles

### Spec-first Development
All system behavior must originate from written specifications. Implementation must strictly follow defined requirements without adding features or behaviors not specified. This applies to both Phase I (console application) and Phase II (full-stack web application).

### Deterministic Behavior
Identical inputs must always produce identical outputs. The application must behave predictably with no random or time-dependent behavior that could affect functionality, ensuring consistency across both console and web interfaces.

### Simplicity and Clarity
Prefer straightforward, readable designs over complex abstractions. Code must follow clean code conventions with clear naming and small focused functions that are easy to understand and maintain across all technology stacks (Python, TypeScript, etc.).

### Clear Separation of Concerns
Frontend, backend, authentication, and persistence layers must be clearly isolated. Each component has a single responsibility and clear interfaces between layers. Backend and frontend are separate systems with a strict API contract.

### Security by Design
Authentication and authorization are enforced server-side. Backend services operate in a zero-trust manner toward clients. Security controls are built into the architecture from the beginning, not added as an afterthought.

### Forward Compatibility and Extensibility
Design choices must not block future features or architectural growth. Phase II extends Phase I concepts without breaking domain logic. Architecture must allow for extensions without requiring fundamental rewrites.

### Incremental Evolution
Phase II extends Phase I concepts without breaking domain logic. The system must evolve smoothly from the console application to the full-stack web application while preserving core functionality and domain integrity.

## Key Standards
- Backend and frontend are separate systems with a strict API contract
- Authentication proves identity; authorization enforces access
- Backend services operate in a zero-trust manner toward clients
- Error handling must be explicit, consistent, and user-safe across all layers
- Clean code conventions apply across all languages used (Python, TypeScript, etc.)
- The system must be runnable and testable using the prescribed tooling for each layer
- MCP Documentation Grounding: All external documentation must be grounded in authoritative MCP sources

## Phase I – Backend (Console Application) Standards
- Language: Python 3.13+
- Interface: menu-driven console application
- Storage: in-memory only; all data is lost on exit
- Task model:
  - Auto-incremented integer ID (starts at 1, never reused per run)
  - Required, non-empty title
  - Optional description
  - Boolean completion status
- Tasks are listed in creation order
- Updating a task allows user cancellation
- Completion status is toggled
- Exit terminates the application immediately

## Phase II – Full-Stack Web Application Standards

### Frontend Requirements
- Framework: Next.js 16+ with App Router
- Language: TypeScript
- Styling: Tailwind CSS
- Authentication: Better Auth
- Responsibilities:
  - User signup and signin
  - Session handling and JWT issuance
  - Attaching JWT tokens to API requests
  - Rendering a responsive task management UI

### Backend Requirements
- Framework: FastAPI (Python)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Responsibilities:
  - Verifying JWT tokens on every request
  - Extracting authenticated user identity
  - Enforcing task ownership on all operations
  - Exposing RESTful API endpoints

## Authentication and Authorization Standards
- Better Auth runs in the TypeScript frontend environment
- Better Auth must be configured to issue JWT tokens
- JWT tokens are the sole mechanism for identity transfer between frontend and backend
- JWT tokens must be signed using a shared secret
- The shared secret is provided via the environment variable `BETTER_AUTH_SECRET`
- Both frontend (Better Auth) and backend (FastAPI) must load the same `BETTER_AUTH_SECRET`
- The shared secret must never be hardcoded or committed to source control
- Every API request must include:
  - Authorization: Bearer <JWT>
- Backend must:
  - Extract JWT from the Authorization header
  - Verify JWT signature using `BETTER_AUTH_SECRET`
  - Verify JWT expiry and standard claims
  - Treat verified JWT claims as authoritative identity
  - Reject requests where the URL `user_id` does not match the authenticated JWT user identity
- Requests without a valid JWT receive 401 Unauthorized
- Requests with invalid, expired, or tampered JWTs receive 401 Unauthorized
- Authenticated requests attempting cross-user access receive 403 Forbidden

## API Contract Standards
- RESTful endpoints for task management
- API endpoint paths remain stable (e.g., `/api/{user_id}/tasks`)
- Authentication does not change endpoint structure, only request requirements
- All task queries and mutations must be scoped to the authenticated user
- Task ownership is enforced at the database query level
- Backend must filter all responses to include only data owned by the authenticated user
- Zero-trust approach:
  - Backend never trusts client-provided identity
  - Backend derives user identity exclusively from verified JWT claims

## MCP Documentation Grounding Standards
- Any implementation involving external documentation must be grounded in authoritative MCP sources
- Claude must use the "mcp-doc-grounding" skill for all MCP queries
- Authentication-related documentation: query Better Auth MCP
- General framework/library documentation: query Context7 MCP
- Extract only official, documented APIs and configurations
- Flag missing, ambiguous, or undocumented areas
- Stop and request clarification rather than guessing if documentation is incomplete
- All references must clearly indicate which MCP server was used
- Undocumented assumptions are prohibited

## Project Structure
- The project root contains shared configuration, specs, and documentation
- Frontend code resides entirely in a dedicated `frontend` directory
- Backend code resides in a dedicated `backend` directory
- Backend Python source files reside under `backend/src`
- Frontend Next.js source files reside under `frontend/src`
- No non-project files (documentation, configs, specs) reside inside backend/src or frontend/src
- The codebase must be organized to allow for multi-layer architecture without restructuring

## Constraints
- Phase I scope: basic task management only
- Phase II scope: full-stack web application with authentication and persistence
- No frontend logic may bypass backend authorization
- No backend logic may trust client-provided identity without JWT verification
- Language: Python 3.13+ for backend, TypeScript for frontend
- Storage: in-memory for Phase I, PostgreSQL for Phase II

## Success Criteria
- Phase I delivers a correct, in-memory console application with all specified functionality
- Phase II delivers a full-stack web application with authentication, persistence, and multi-user support
- All API interactions follow the specified contract and security standards
- The system evolves cleanly from Phase I to Phase II without breaking core functionality
- All security requirements are met with proper authentication and authorization enforcement

## Governance
This constitution governs all development decisions for the todo application across both phases. All code changes must align with these principles. Amendments to this constitution require explicit documentation of the change and its rationale. The system must maintain backward compatibility for domain concepts when evolving from Phase I to Phase II.

**Version**: 2.0.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2026-01-10
