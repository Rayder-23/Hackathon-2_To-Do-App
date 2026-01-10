# Implementation Plan: Todo Application – Phase II: Full-Stack Web System

**Branch**: `2-todo-phase-2` | **Date**: 2026-01-11 | **Spec**: specs/2-todo-phase-2/spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the Phase I in-memory console todo application into a full-stack, multi-user web application with persistent storage and authentication. The implementation will use Next.js/TypeScript/Tailwind/Better Auth for the frontend, and FastAPI/SQLModel/PostgreSQL for the backend with JWT-based authentication and strict separation of concerns.

## Technical Context

**Language/Version**: Python 3.13+ (Backend), TypeScript (Frontend)
**Primary Dependencies**: Next.js 16+, FastAPI, SQLModel, Better Auth, PostgreSQL
**Storage**: Neon Serverless PostgreSQL database with foreign key relationships
**Testing**: pytest (Backend), Jest/Vitest (Frontend)
**Target Platform**: Web application supporting 320px to 1920px screen sizes
**Project Type**: Web (dual: frontend + backend)
**Performance Goals**: Handle ≥1000 concurrent users with response time ≤3 seconds, JWT validation ≤100ms average
**Constraints**: All API endpoints require valid JWT tokens, users can only access own tasks, soft deletion with 30-day retention, rate limiting at 100 req/hr per IP AND 500 req/hr per authenticated user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Security by Design**: Authentication and authorization are enforced server-side with zero-trust approach - PASSED
2. **Separation of Concerns**: Clear isolation between frontend, backend, authentication, and persistence layers - PASSED
3. **Forward Compatibility**: Architecture allows extensions without fundamental rewrites - PASSED
4. **Deterministic Behavior**: Identical inputs will produce identical outputs - PASSED
5. **Clean Code Conventions**: Will follow clean code principles across all languages - PASSED

## Project Structure

### Documentation (this feature)

```text
specs/2-todo-phase-2/
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
│   │   ├── user.py
│   │   ├── task.py
│   │   └── base.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   └── user_service.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── tasks.py
│   │   └── middleware/
│   │       └── auth_middleware.py
│   └── database/
│       └── session.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   ├── tasks/
│   │   └── ui/
│   ├── pages/
│   │   ├── auth/
│   │   └── dashboard/
│   ├── services/
│   │   ├── api-client.ts
│   │   └── auth-service.ts
│   ├── lib/
│   │   └── utils.ts
│   └── types/
│       └── index.ts
├── public/
├── styles/
└── tests/
```

**Structure Decision**: Web application with separate backend and frontend directories as specified in the constitution. Backend handles all authentication enforcement and data access control, while frontend manages UI rendering and JWT storage/sending.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |