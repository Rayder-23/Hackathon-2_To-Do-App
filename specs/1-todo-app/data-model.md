# Data Model: In-Memory Todo Console Application

## Task Entity

### Attributes
- **id** (int): Auto-incremented unique identifier for each task
  - Auto-generated starting from 1
  - Never reused after deletion
  - Required, positive integer
- **title** (str): Required non-empty title for the task
  - Must contain at least one non-whitespace character
  - Required field
  - Maximum flexibility on content
- **description** (str): Optional description for the task
  - Can be empty or None
  - Optional field
  - Maximum flexibility on content
- **completed** (bool): Boolean indicating completion status
  - Default value: False
  - Indicates whether the task is complete (True) or incomplete (False)

### Validation Rules
1. **Title validation**: Title must be non-empty (at least one non-whitespace character)
2. **ID uniqueness**: Each ID must be unique within the application session
3. **ID sequence**: IDs are assigned sequentially starting from 1
4. **ID persistence**: Once assigned, IDs are never reused even after task deletion

### State Transitions
- **Creation**: New task created with `completed=False`
- **Status Toggle**: `completed` field toggles between True and False
- **Deletion**: Task is removed from storage but ID is not reused

### Relationships
- No relationships with other entities (standalone entity)

### Lifecycle
1. **Create**: Task is initialized with title, optional description, and completed=False
2. **Read**: Task data is accessed for display or validation
3. **Update**: Title or description can be modified
4. **Delete**: Task is removed from storage
5. **Toggle**: Completion status is flipped

## Storage Model

### In-Memory Repository
- **Primary Storage**: Dictionary mapping ID to Task objects for O(1) lookup
- **Order Preservation**: List of Task objects in creation order
- **ID Counter**: Integer counter for next available ID

### Operations
- **Create**: Add task to dictionary and list, increment ID counter
- **Read**: Access task by ID from dictionary or iterate through list
- **Update**: Modify task attributes in dictionary
- **Delete**: Remove task from dictionary and list, do not reuse ID
- **List All**: Return all tasks in creation order