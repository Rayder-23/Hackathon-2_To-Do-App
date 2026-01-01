---
description: "Task list for todo console application implementation"
---

# Tasks: In-Memory Todo Console Application

**Input**: Design documents from `/specs/1-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure per implementation plan
- [x] T002 [P] Create backend/src directory structure
- [x] T003 [P] Create backend/src/todo directory
- [x] T004 Create main.py application entry point

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create Task model in backend/src/todo/models.py
- [x] T006 Create in-memory repository in backend/src/todo/repository.py
- [x] T007 Create basic CLI structure in backend/src/todo/cli.py
- [x] T008 Create main application flow in backend/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: User can create new tasks with a required title and optional description through the console menu interface

**Independent Test**: User can start the application, select the add task option, enter a title and optional description, and see the task appear in the task list with an auto-generated ID

### Implementation for User Story 1

- [x] T009 [P] [US1] Implement Task model with validation in backend/src/todo/models.py
- [x] T010 [P] [US1] Implement add_task method in backend/src/todo/repository.py
- [x] T011 [US1] Implement add_task business logic in backend/src/todo/services.py
- [x] T012 [US1] Implement add task menu option in backend/src/todo/cli.py
- [x] T013 [US1] Connect add task flow from CLI to services to repository

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: User can view all tasks with their ID, title, description (if present), and completion status in creation order

**Independent Test**: User can view all tasks in the system, displayed in the order they were created, with all relevant information clearly presented

### Implementation for User Story 2

- [x] T014 [P] [US2] Implement get_all_tasks method in backend/src/todo/repository.py
- [x] T015 [US2] Implement get_all_tasks business logic in backend/src/todo/services.py
- [x] T016 [US2] Implement view all tasks menu option in backend/src/todo/cli.py
- [x] T017 [US2] Connect view tasks flow from CLI to services to repository
- [x] T018 [US2] Implement structured list output with clear labels in backend/src/todo/cli.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Update and Manage Tasks (Priority: P2)

**Goal**: User can update existing tasks, delete tasks with confirmation, or toggle task completion status

**Independent Test**: User can modify existing tasks by updating them, marking them as complete/incomplete, or removing them from the list with appropriate confirmation

### Implementation for User Story 3

- [x] T019 [P] [US3] Implement update_task method in backend/src/todo/repository.py
- [x] T020 [P] [US3] Implement delete_task method in backend/src/todo/repository.py
- [x] T021 [P] [US3] Implement toggle_task_completion method in backend/src/todo/repository.py
- [x] T022 [US3] Implement update_task business logic in backend/src/todo/services.py
- [x] T023 [US3] Implement delete_task business logic in backend/src/todo/services.py
- [x] T024 [US3] Implement toggle_task business logic in backend/src/todo/services.py
- [x] T025 [US3] Implement update task menu option in backend/src/todo/cli.py
- [x] T026 [US3] Implement delete task menu option in backend/src/todo/cli.py
- [x] T027 [US3] Implement toggle task menu option in backend/src/todo/cli.py
- [x] T028 [US3] Connect all management flows from CLI to services to repository

**Checkpoint**: All user stories should now be independently functional

---
## Phase 6: Error Handling and Validation (Cross-cutting concerns)

**Goal**: Implement proper error handling and validation across all features

**Independent Test**: Application handles invalid user input gracefully without crashing

- [x] T029 [P] [US1] Add title validation to ensure non-empty requirement in backend/src/todo/models.py
- [x] T030 [P] [US1] Add validation error handling in backend/src/todo/services.py
- [x] T031 [US3] Implement task existence validation for update/delete operations
- [x] T032 [US3] Add confirmation prompt for delete operation
- [x] T033 [US3] Implement update cancellation functionality
- [x] T034 Implement graceful error handling that returns to main menu

---
## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T035 Add menu navigation loop functionality to return to main menu after each operation
- [x] T036 Implement proper ID management with auto-increment and no reuse after deletion
- [x] T037 Add empty task list handling for view operation
- [x] T038 [P] Add docstrings and comments for all functions
- [x] T039 [P] Format output to match structured list with clear labels requirement
- [x] T040 Run quickstart validation to ensure application runs with uv

---
## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Error Handling (Phase 6)**: Depends on core functionality implementation
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May depend on US1 models but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May depend on US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before CLI implementation
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---
## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "T009 [P] [US1] Implement Task model with validation in backend/src/todo/models.py"
Task: "T010 [P] [US1] Implement add_task method in backend/src/todo/repository.py"
```

---
## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence