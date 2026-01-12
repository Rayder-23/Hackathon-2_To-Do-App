# Todo Application - Phase II

A full-stack web application with authentication and task management capabilities built using Next.js, FastAPI, and BetterAuth.

## Features

- **User Authentication**: Secure user registration and login with BetterAuth
- **Task Management**: Create, read, update, delete, and toggle completion of tasks
- **User Isolation**: Users can only access their own tasks
- **Soft Deletion**: Tasks are marked as deleted but retained for 30 days
- **Responsive UI**: Mobile-friendly interface built with Tailwind CSS
- **JWT Authentication**: Secure API access with JWT tokens
- **RFC 7807 Error Handling**: Standardized error responses

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, Python
- **Database**: PostgreSQL (via Neon)
- **Authentication**: BetterAuth with JWT tokens
- **Styling**: Tailwind CSS

## Architecture

### Frontend Structure
- `/pages`: Next.js pages router (auth pages, dashboard)
- `/components`: Reusable UI components (auth forms, task components)
- `/services`: Business logic (auth service, API client)
- `/types`: TypeScript type definitions

### Backend Structure
- `/api`: API routes and middleware
- `/models`: Database models (User, Task)
- `/services`: Business logic (user service, task service, auth service)
- `/database`: Database session management

## Setup

### Environment Variables

Create `.env` files in both frontend and backend:

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

**Backend (.env):**
```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
BETTER_AUTH_SECRET=your_secret_key
JWT_SECRET=your_jwt_secret
```

### Running the Application

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn src.main:app --reload --port 8000
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login user

### Tasks (Require Authentication)
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Soft delete task
- `PATCH /api/{user_id}/tasks/{task_id}/toggle` - Toggle task completion
- `GET /api/{user_id}/tasks/deleted` - Get soft-deleted tasks

## Security Features

- JWT token validation with required claims (sub, email, exp, iat)
- User isolation - users can only access their own resources
- Input validation and sanitization
- RFC 7807 Problem Details for error responses
- Rate limiting (planned)

## Error Handling

The application follows RFC 7807 for error responses with standardized error formats:

```json
{
  "title": "Bad Request",
  "status": 400,
  "detail": "Task title exceeds maximum length of 255 characters"
}
```

## Development

The project follows a spec-driven development approach with implementation tasks tracked in the specs directory. All components are tested for integration and functionality.

## Testing

To run tests (when implemented):
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT