# Quickstart Guide: Todo Application Phase II

## Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL (or Neon Serverless PostgreSQL)
- Better Auth compatible environment

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
# Already in the repository root
cd E:\RY Documents\Ry Coding\Gov IT\GovIT Quarter 4 (Gemini CLI)\Hackathon-II\todo-app
```

### 2. Backend Setup

```bash
# Navigate to backend directory (create if it doesn't exist)
mkdir -p backend/src
cd backend

# Install Python dependencies
uv add fastapi[standard] sqlmodel psycopg2-binary python-dotenv

# Set up environment variables
echo "DATABASE_URL=postgresql://user:password@localhost/dbname" > .env
echo "BETTER_AUTH_SECRET=your-secret-key-here" >> .env
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install frontend dependencies
npm install better-auth
# Other dependencies will be installed during Next.js setup
```

### 4. Environment Configuration

Create `.env` files for both backend and frontend with the following variables:

**Backend (.env)**:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
```

**Frontend (.env.local)**:
```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 5. Run the Applications

**Backend**:
```bash
cd backend
# Start the FastAPI server
uvicorn src.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
# Start the Next.js development server
npm run dev
```

## Key Architecture Components

### Backend Structure
- `models/`: SQLModel database models
- `services/`: Business logic for auth, tasks, users
- `api/routes/`: API endpoint definitions
- `api/middleware/`: Authentication middleware
- `database/`: Database session management

### Frontend Structure
- `components/`: Reusable UI components
- `pages/`: Next.js pages for routing
- `services/`: API client and auth service
- `types/`: TypeScript type definitions

## API Endpoints

### Authentication
- `POST /api/users/register` - User registration
- `POST /api/users/login` - User login

### Task Management
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create task for user
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Soft-delete task
- `PATCH /api/{user_id}/tasks/{task_id}/toggle` - Toggle completion
- `GET /api/{user_id}/tasks/deleted` - Get deleted tasks

## Authentication Flow

1. User registers/logs in via Better Auth
2. JWT token is issued and stored in httpOnly cookie
3. For API requests, token is automatically attached via auth middleware
4. Backend verifies JWT signature and extracts user identity
5. Backend enforces that user can only access their own tasks

## Development Workflow

1. Implement backend models and services first
2. Create API endpoints with proper authentication
3. Develop frontend components to interact with API
4. Test authentication and authorization flows
5. Verify cross-user access prevention

## Testing Strategy

- Unit tests for individual components
- Integration tests for API endpoints
- End-to-end tests for complete user flows
- Security tests for authentication and authorization