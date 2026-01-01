# Quickstart Guide: In-Memory Todo Console Application

## Prerequisites

- Python 3.13+ installed
- uv package manager installed

## Setup

1. **Clone the repository** (if applicable) or navigate to the project directory
2. **Install dependencies** (if any external packages are added later):
   ```bash
   uv sync
   ```

## Running the Application

To run the application:

```bash
uv run backend/main.py
```

Or if the project is set up as a package:

```bash
uv run python -m todo.main
```

## Using the Application

Once the application starts, you'll see a menu with numbered options:

```
Todo Application Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Exit
```

### Adding a Task
1. Select option `1`
2. Enter the task title (required)
3. Optionally enter a description
4. The task will be created with an auto-incremented ID

### Viewing Tasks
1. Select option `2`
2. All tasks will be displayed in creation order
3. Each task shows ID, title, description (if present), and completion status

### Updating a Task
1. Select option `3`
2. Enter the task ID you want to update
3. Enter the new title and/or description
4. Or type 'cancel' to abort the operation

### Deleting a Task
1. Select option `4`
2. Enter the task ID you want to delete
3. Confirm the deletion when prompted
4. The task will be removed from the list

### Toggling Task Completion
1. Select option `5`
2. Enter the task ID you want to modify
3. The completion status will be toggled (complete ↔ incomplete)

### Exiting
1. Select option `6`
2. The application will terminate

## Example Workflow

```
Todo Application Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Exit
Choose an option: 1
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
Task added successfully with ID 1!

Todo Application Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Exit
Choose an option: 2
Tasks:
ID: 1, Title: Buy groceries, Description: Milk, eggs, bread, Completed: False

Todo Application Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Exit
Choose an option: 5
Enter task ID to toggle: 1
Task 1 completion status toggled!

Todo Application Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Exit
Choose an option: 2
Tasks:
ID: 1, Title: Buy groceries, Description: Milk, eggs, bread, Completed: True

Todo Application Menu:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Exit
Choose an option: 6
Goodbye!
```

## Error Handling

- If you enter invalid input, you'll see a clear error message
- The application will return to the main menu after any error
- The application will never crash due to invalid user input

## Important Notes

- All data is stored in memory only and will be lost when the application exits
- Task IDs start at 1 and increment sequentially
- Deleted task IDs are never reused within the same application session
- You can cancel update operations by typing 'cancel' when prompted