# Data Model: Todo Application Phase II

## Entity: User

**Fields**:
- `id` (Integer, Primary Key, Auto-increment) - Unique identifier for the user
- `email` (String, Unique, Required) - User's email address (max 255 chars)
- `hashed_password` (String, Required) - Hashed password (max 1000 chars)
- `created_at` (DateTime, Required) - Timestamp when user was created
- `updated_at` (DateTime, Required) - Timestamp when user was last updated

**Constraints**:
- Email must be unique across the system
- Email format must match /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
- Password must meet complexity requirements (minimum 8 chars with uppercase, lowercase, number, special char)

**Relationships**:
- One-to-Many: User has many Tasks (user.tasks)

## Entity: Task

**Fields**:
- `id` (Integer, Primary Key, Auto-increment) - Unique identifier for the task
- `title` (String, Required) - Task title (max 255 chars)
- `description` (String, Optional) - Task description (max 1000 chars)
- `completed` (Boolean, Required, Default: false) - Completion status
- `user_id` (Integer, Foreign Key, Required) - Owner of the task
- `created_at` (DateTime, Required) - Timestamp when task was created
- `updated_at` (DateTime, Required) - Timestamp when task was last updated
- `deleted_at` (DateTime, Optional) - Timestamp when task was soft-deleted

**Constraints**:
- Title is required and max 255 characters
- Description is optional and max 1000 characters
- Completed defaults to false
- user_id references User.id with foreign key constraint
- Tasks cannot change ownership after creation

**Relationships**:
- Many-to-One: Task belongs to User (task.user)

## Entity: Authentication Token

**Fields**:
- `user_id` (Integer, Foreign Key, Required) - Associated user
- `token` (String, Required) - JWT token string
- `expires_at` (DateTime, Required) - Expiration timestamp
- `created_at` (DateTime, Required) - Timestamp when token was created

**Constraints**:
- JWT tokens expire after 24 hours
- Refresh tokens valid for 7 days
- Token must be signed using BETTER_AUTH_SECRET

## Validation Rules

**User Validation**:
- Email uniqueness must be enforced at database level
- Email format validation on creation/update
- Password complexity validation on creation/update

**Task Validation**:
- Title length validation (1-255 characters)
- Description length validation (0-1000 characters)
- User_id must reference a valid user
- Only owner can modify task

**Authentication Validation**:
- JWT signature verification using BETTER_AUTH_SECRET
- JWT claim validation (sub, email, exp, iat)
- Token expiration validation

## State Transitions

**Task State Transitions**:
- Active → Completed: When toggle completion status
- Active → Soft-deleted: When delete task (sets deleted_at)
- Soft-deleted → Active: Not allowed (permanent deletion only via admin)

## Indexes

**Required Indexes**:
- User.email (unique index for fast lookups)
- Task.user_id (index for user-specific queries)
- Task.deleted_at (index for soft deletion queries)
- Authentication Token.expires_at (index for token expiration checks)