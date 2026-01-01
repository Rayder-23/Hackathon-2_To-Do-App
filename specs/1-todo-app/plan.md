# Implementation Plan: In-Memory Todo Console Application

**Branch**: `1-todo-app` | **Date**: 2026-01-01 | **Spec**: [link]
**Input**: Feature specification from `/specs/1-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a menu-driven console application for managing todo tasks in memory. The application will follow a clean architecture with clear separation of concerns between data models, business logic, and user interface. The system will support task creation, viewing, updating, deletion, and completion status toggling with proper error handling and user experience.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Standard library only (no external dependencies)
**Storage**: In-memory using Python data structures
**Testing**: Manual testing based on specification acceptance scenarios
**Target Platform**: Cross-platform console application
**Project Type**: Single console application - follows backend structure
**Performance Goals**: Sub-second response time for all operations
**Constraints**: <200ms p95 for operations, <100MB memory usage, console-only interface
**Scale/Scope**: Single user, single session, up to 1000 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-driven Implementation: All functionality will be implemented based on the feature specification
- ✅ Deterministic Logic: Operations will produce consistent results for identical inputs
- ✅ Simplicity and Clarity: Clean, readable code with focused functions
- ✅ Separation of Concerns: Clear separation between models, repository, services, and CLI
- ✅ Forward Compatibility: Architecture supports future persistence and frontend integration
- ✅ Error Handling and User Experience: Defensive error handling with user-friendly messages

## Project Structure

### Documentation (this feature)

```text
specs/1-todo-app/
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
│   └── todo/
│       ├── models.py        # Task data definitions
│       ├── repository.py    # In-memory task storage
│       ├── services.py      # Business logic and rules
│       └── cli.py           # Menu-driven console interface
└── main.py                # Application entry point
```

**Structure Decision**: Backend-only structure with clear separation of concerns following the canonical layout from the constitution.

## Architecture Overview

The application follows a clean architecture pattern with clear separation of concerns:

1. **Models Layer**: Defines the Task data structure with validation
2. **Repository Layer**: Manages in-memory storage of tasks with CRUD operations
3. **Services Layer**: Implements business logic and rules for task operations
4. **CLI Layer**: Handles user input/output and menu navigation
5. **Main Entry Point**: Orchestrates the application flow

**Data Flow**: User Input → CLI → Services → Repository → Models → Services → CLI → Output

## Component Breakdown

### Task Model Definition
- `Task` class with attributes: id (int), title (str), description (str, optional), completed (bool)
- Validation: Title must be non-empty, description can be empty
- Auto-incrementing ID management with no reuse after deletion

### In-Memory Storage Mechanism
- Singleton repository pattern using Python dictionary for O(1) lookup
- Task list for maintaining creation order
- ID counter for auto-incrementing IDs
- Thread-safe operations (not needed for single-user console app)

### Business Logic for Features
- **Add Task**: Validate title, create task with next available ID, add to storage
- **View Tasks**: Return all tasks in creation order
- **Update Task**: Validate existence, allow cancellation, update fields
- **Delete Task**: Validate existence, require confirmation, remove from storage
- **Toggle Status**: Validate existence, flip completion status

### Menu-Driven CLI Control Loop
- Main menu with numbered options (1-6)
- Loop-based interface that returns to main menu after each operation
- Clear error messages and return to main menu on invalid input
- Structured output with clear labels for each task field

## Feature-to-Component Mapping

### Add Task
- **CLI**: Prompt for title and description, validate input
- **Services**: Validate title is non-empty, create task
- **Repository**: Store task, increment ID counter
- **Models**: Create Task instance with validation

### View Tasks
- **CLI**: Format and display tasks in structured list
- **Services**: Retrieve all tasks in creation order
- **Repository**: Return all tasks in insertion order
- **Models**: Access task attributes for display

### Update Task (with cancel support)
- **CLI**: Prompt for task ID, allow cancellation, get new values
- **Services**: Validate task exists, validate new title, update task
- **Repository**: Update task in storage
- **Models**: Update task attributes with validation

### Delete Task (with confirmation)
- **CLI**: Prompt for task ID, confirm deletion
- **Services**: Validate task exists, perform deletion
- **Repository**: Remove task from storage
- **Models**: No direct interaction

### Toggle Completion Status
- **CLI**: Prompt for task ID
- **Services**: Validate task exists, toggle status
- **Repository**: Update task completion status
- **Models**: Toggle completion attribute

## Decision Log

### Key Design Decisions

1. **In-Memory Storage**: Using Python dict and list for O(1) access and ordered storage
   - **Rationale**: Meets requirement for in-memory only storage, simple implementation
   - **Future Expansion**: Repository interface allows easy swap to file/DB storage

2. **Auto-Incrementing IDs**: Using a counter that never reuses IDs after deletion
   - **Rationale**: Matches specification requirement that IDs are never reused
   - **Future Expansion**: Supports audit trails and external references

3. **Separation of Concerns**: Clear layering of models, repository, services, and CLI
   - **Rationale**: Aligns with constitution principle, enables testability
   - **Future Expansion**: Each layer can be modified independently

4. **Menu-Driven Interface**: Loop-based with numbered options
   - **Rationale**: Matches specification clarification, simple to implement and use
   - **Future Expansion**: Menu structure supports adding new features

### Alternatives Considered

- **Storage**: Considered using only a list vs. dictionary + list. Chose dict + list for fast lookups while preserving order
- **Input Method**: Considered command-line arguments vs. interactive menu. Chose menu for better UX
- **Error Handling**: Considered different error recovery strategies. Chose to always return to main menu

## Validation and Testing Strategy

### Manual Test Scenarios Mapped to Success Criteria

**SC-001: Users can add a new task in under 30 seconds**
- Manual test: Time task creation from menu selection to completion
- Expected: <30 seconds for title and optional description entry

**SC-002: All tasks displayed with 100% accuracy**
- Manual test: Create tasks with various titles, descriptions, and statuses
- Expected: All attributes displayed exactly as entered

**SC-003: 95% of operations complete successfully**
- Manual test: Execute all operations multiple times with valid and invalid inputs
- Expected: No crashes, clear error messages for invalid inputs

**SC-004: Tasks listed in creation order**
- Manual test: Create multiple tasks and verify ordering
- Expected: Tasks appear in order of creation (first created first in list)

**SC-005: Application runs using uv command**
- Manual test: Run application with `uv run` command
- Expected: Application starts without errors

### Edge Cases Testing

- **Invalid task IDs**: Test update/delete with non-existent IDs
- **Empty/whitespace titles**: Test task creation with invalid titles
- **Canceled updates**: Test update cancellation functionality
- **Empty task list**: Test viewing tasks when none exist
- **Invalid menu selections**: Test non-numeric and out-of-range menu choices

### Behavioral Checks

- **Error handling**: Verify application doesn't crash on invalid input
- **Confirmation prompts**: Verify delete confirmation works correctly
- **Menu navigation**: Verify return to main menu after each operation
- **Cancellation**: Verify update cancellation functionality
- **ID management**: Verify IDs are not reused after deletion

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |