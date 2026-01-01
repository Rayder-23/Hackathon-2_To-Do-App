<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution for todo app)
- List of modified principles: N/A (new constitution)
- Added sections: Core Principles (6), Key Standards, Functional Rules, Project Structure, Constraints, Success Criteria, Governance
- Removed sections: None (new constitution)
- Templates requiring updates: N/A (initial creation)
- Follow-up TODOs: [RATIFICATION_DATE] needs to be set
-->
# In-Memory Todo Console Application Constitution

## Core Principles

### Spec-driven Implementation
All system behavior must be derived from written specifications. Implementation must strictly follow defined requirements without adding features or behaviors not specified.

### Deterministic Logic
Identical inputs must always yield identical results. The application must behave predictably with no random or time-dependent behavior that could affect functionality.

### Simplicity and Clarity
Prefer straightforward, readable designs over complex abstractions. Code must follow clean code conventions with clear naming and small focused functions that are easy to understand and maintain.

### Separation of Concerns
Data models, business logic, and user interaction must be clearly isolated. Each component has a single responsibility and clear interfaces between layers.

### Forward Compatibility
Design choices must not prevent future persistence or frontend integration. Architecture must allow for extensions without requiring fundamental rewrites.

### Error Handling and User Experience
Error handling must be defensive and user-friendly; invalid input must never crash the program. The application must provide clear, helpful feedback to users.

## Key Standards
- The application is a menu-driven, console-based program
- Task data is stored strictly in memory and is discarded on application exit
- Error handling must be defensive and user-friendly; invalid input must never crash the program
- Python code must follow clean code conventions (clear naming, small focused functions)
- uv must be used as the project's Python environment and dependency manager
- The project must be runnable using uv without additional tooling assumptions

## Functional Rules
- A task consists of: An auto-incremented integer ID, a required non-empty title, an optional description, and a boolean completion status
- Task IDs start at 1, increment monotonically, and are never reused within a single run
- Tasks are listed in creation order
- Updating a task allows the user to cancel the operation before completion
- Marking a task complete toggles its completion state (complete ↔ incomplete)
- Selecting the exit option terminates the application immediately

## Project Structure
- All Python source code must reside under a backend/src directory
- Only Python source files are placed inside backend/src
- No non-Python project files (documentation, configs, specs) reside inside backend/src
- The backend codebase must be organized to allow future frontend integration without restructuring

## Constraints
- Language: Python 3.13+
- Interface: console only
- Storage: in-memory only
- Scope: basic todo functionality (add, view, update, delete, mark complete)

## Success Criteria
- All defined features behave exactly as specified
- User interactions are clear, predictable, and error-tolerant
- The application runs successfully via uv from the command line
- The backend structure is clean, minimal, and extensible

## Governance
This constitution governs all development decisions for the todo application. All code changes must align with these principles. Amendments to this constitution require explicit documentation of the change and its rationale.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2026-01-01
