---
id: 9
title: Amend Constitution Fullstack
stage: constitution
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Rayder
command: sp.constitution
labels: ["constitution", "todo-app", "full-stack", "phase-ii"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
Project: Todo Application – Spec-Driven Backend + Full-Stack Web System

This constitution governs both:
- Phase I: In-memory, console-based Python backend
- Phase II: Full-stack, multi-user web application with authentication and persistence

Core principles:
- Spec-first development: all system behavior must originate from written specifications
- Deterministic behavior: identical inputs must always produce identical outputs
- Clear separation of concerns: frontend, backend, authentication, and persistence are isolated
- Security by design: authentication and authorization are enforced server-side
- Incremental evolution: Phase II extends Phase I concepts without breaking domain logic
- Extensibility: design decisions must not block future features or architectural growth

Key standards:
- Backend and frontend are separate systems with a strict API contract
- Authentication proves identity; authorization enforces access
- Backend services operate in a zero-trust manner toward clients
- Error handling must be explicit, consistent, and user-safe
- Clean code conventions apply across all languages used
- The system must be runnable and testable using the prescribed tooling for each layer

Phase I – Backend (Console Application):
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

Phase II – Full-Stack Web Application:

Frontend:
- Framework: Next.js 16+ with App Router
- Language: TypeScript
- Styling: Tailwind CSS
- Authentication: Better Auth
- Responsibilities:
  - User signup and signin
  - Session handling and JWT issuance
  - Attaching JWT tokens to API requests
  - Rendering a responsive task management UI

Backend:
- Framework: FastAPI (Python)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Responsibilities:
  - Verifying JWT tokens on every request
  - Extracting authenticated user identity
  - Enforcing task ownership on all operations
  - Exposing RESTful API endpoints

Authentication and Authorization:
- Better Auth runs in the TypeScript frontend environment
- Better Auth must be configured to issue JWT tokens
- JWT tokens are the sole mechanism for identity transfer between frontend and backend
- Every API request must include:
  - Authorization: Bearer <JWT>
- Backend must:
  - Verify JWT signature and expiry
  - Treat JWT claims as authoritative
  - Reject requests where the URL user_id does not match the JWT user identity
- Requests without valid JWTs receive 401 Unauthorized
- Ownership violations receive 403 Forbidden

MCP Documentation Grounding (Mandatory):
- Any implementation involving external documentation must be grounded in authoritative MCP sources
- Claude must use the **"mcp-doc-grounding" skill** for all MCP queries
- Skill behavior:
  - Authentication-related documentation: query Better Auth MCP
  - General framework/library documentation: query Context7 MCP
  - Extract only official, documented APIs and configurations
  - Flag missing, ambiguous, or undocumented areas
  - Stop and request clarification rather than guessing if documentation is incomplete
- All references must clearly indicate which MCP server was used
- Undocumented assumptions are prohibited

API Standards (Phase II):
- RESTful endpoints for task management
- All task queries and mutations must be scoped to the authenticated user
- Task ownership is enforced at the database query level
- Endpoint structure remains stable, but behavior is user-scoped after authentication

Project directory structure:
- The project root contains shared configuration, specs, and documentation
- Frontend code resides entirely in a dedicated `frontend` directory
- Backend code resides in a dedicated `backend` directory
- Backend Python source files reside under `backend/src`
- Frontend Next.js source files reside under `frontend/src`

Constraints:
- Phase I scope: basic task management only
- Phase II scope: full-stack web application with authentication and persistence
- No frontend logic may bypass backend authorization
- No backend logic may trust client-provided identity without JWT verification

Success criteria:
- Phase I delivers a correct, in-me
```

## Response snapshot

Updated the project constitution to version 2.0.0 to encompass both Phase I (console application) and Phase II (full-stack web application). The updated constitution now includes:

- Expanded core principles to cover both phases
- Detailed standards for both backend (Phase I) and full-stack (Phase II) development
- Authentication and Authorization standards for the web application
- API Contract Standards for secure communication
- MCP Documentation Grounding requirements
- Updated project structure to accommodate frontend/backend separation
- Success criteria for both phases

The constitution now serves as the governing document for the complete evolution from the console application to the full-stack web application with authentication and persistence.

## Outcome

- ✅ Impact: Major constitution update from v1.0.0 to v2.0.0 to include full-stack web application
- 🧪 Tests: No tests required for constitution update
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive changes
- 🔁 Next prompts: Ready to proceed with Phase II specification and planning
- 🧠 Reflection: Constitution now covers complete project lifecycle from console to web app

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution successfully updated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase II specification using updated constitution