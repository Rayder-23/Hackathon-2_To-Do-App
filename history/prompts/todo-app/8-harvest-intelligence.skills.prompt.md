---
id: 8
title: Harvest Intelligence
stage: misc
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-app
branch: 1-todo-app
user: Rayder
command: sp.phr
labels: ["intelligence", "skills", "python-debugging", "todo-app"]
links:
  spec: specs/1-todo-app/spec.md
  plan: specs/1-todo-app/plan.md
  tasks: specs/1-todo-app/tasks.md
  ticket: null
  adr: null
  pr: null
files:
 - .claude/skills/python-project-debugger/SKILL.md
 - backend/main.py
 - history/prompts/todo-app/7-analyze-fix-import-error.red.prompt.md
tests:
 - none
---

## Prompt

```text
I'd like to harvest intelligence from this sesion, use the 'session-intelligence-harvester' skill in '.claude' and tell me valuable intelligence that should be used to make skills
```

## Response snapshot

Successfully harvested intelligence from the session and created a new skill: python-project-debugger. The session involved fixing a Python module import error where 'from todo.cli import TodoCLI' failed with ModuleNotFoundError.

The intelligence harvest resulted in:
1. Analysis of the import error and its solution (adding backend/src to Python path)
2. Creation of a reusable python-project-debugger skill in .claude/skills/
3. Documentation of the solution in the PHR system

The new skill provides systematic debugging for Python import errors, module not found errors, path configuration issues, and other Python project structure problems.

## Outcome

- ✅ Impact: Created reusable skill for Python import debugging
- 🧪 Tests: No automated tests needed for this skill creation
- 📁 Files: Created python-project-debugger skill and updated main.py
- 🔁 Next prompts: Use the new skill for future Python import issues
- 🧠 Reflection: Session intelligence successfully converted to reusable skill

## Evaluation notes (flywheel)

- Failure modes observed: Python path configuration issues are common in multi-directory projects
- Graders run and results (PASS/FAIL): New skill created and documented
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Apply the new skill to other Python projects with similar issues