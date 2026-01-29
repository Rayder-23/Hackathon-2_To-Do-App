---
id: 1
title: Todo Mini Phase 2.5 Specification Creation
stage: spec
date_iso: 2026-01-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-phase-2.5
branch: main
user: Rayder
command: /sp.specify
labels: ["specify", "feature-creation", "auth-alignment", "backend", "frontend", "authentication"]
links
  spec: "specs\2.5-auth-alignment\spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs\2.5-auth-alignment\spec.md"
  - "specs\2.5-auth-alignment\checklists\requirements.md"
tests_yaml:
  - none
---

# Todo Mini Phase 2.5 Specification Creation

## Prompt Text
Mini Phase 2.5: Backend–Frontend Authentication Alignment

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
- All external documentation must be MCP-grounded
- Claude must use the "Context7" or "BetterAuth" MCP Servers when consulting documentation

## Response Text
Created feature specification for backend-frontent authentication alignment with BetterAuth and FastAPI.

## Outcome Impact
Successfully created the feature specification file and checklist for the auth-alignment feature, establishing proper structure for the authentication alignment work between BetterAuth frontend and FastAPI backend.

## Tests Summary
none

## Files Summary
- Created specs/2.5-auth-alignment/spec.md with complete feature specification
- Created specs/2.5-auth-alignment/checklists/requirements.md with validation checklist

## Next Prompts
none

## Reflection Note
The sp.specify command successfully created the feature specification with proper structure and validation checklist.

## Failure Modes Observed
none

## Next Experiment to Improve Prompt Quality
none