from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from ...database.session import get_session
from ...models.task import Task, TaskBase
from ...services.task_service import TaskService
from ...api.middleware.auth_middleware import get_current_user, verify_user_access
from pydantic import BaseModel

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


@router.get("/{user_id}/tasks")
def get_tasks(user_id: str, db: Session = Depends(get_session), jwt_sub: str = Depends(get_current_user)):
    """
    Retrieve user's tasks (sorted by creation date).
    Implements FR-004: Users MUST be able to view their complete todo list sorted by creation date (most recent first)
    Implements FR-009: System MUST enforce authentication for all API endpoints with valid JWT tokens
    Implements FR-010: System MUST ensure users can only access their own tasks and MUST return appropriate HTTP 403 Forbidden errors when unauthorized access is attempted
    Implements FR-023: System MUST filter all responses to include only data owned by authenticated user
    """
    # Enforce user isolation: path user_id must match JWT sub
    if jwt_sub != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    # Convert user_id to int for database operations
    user_id_int = int(user_id)
    # Enforce ownership at DB layer: only return tasks for authenticated user
    tasks = TaskService.get_tasks_for_user(db, user_id_int)
    return tasks


@router.post("/{user_id}/tasks")
def create_task(user_id: str, task_data: TaskCreate, db: Session = Depends(get_session), jwt_sub: str = Depends(get_current_user)):
    """
    Create new task for user.
    Implements FR-003: Users MUST be able to add new tasks to their personal todo list with titles up to 255 characters and descriptions up to 1000 characters
    Implements FR-003.1: System MUST return HTTP 400 Bad Request when task title exceeds 255 characters
    Implements FR-003.2: System MUST return HTTP 400 Bad Request when task description exceeds 1000 characters
    Implements FR-009: System MUST enforce authentication for all API endpoints with valid JWT tokens
    Implements FR-010: System MUST ensure users can only access their own tasks
    """
    # Enforce user isolation: path user_id must match JWT sub
    if jwt_sub != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only create tasks for yourself"
        )

    # Validate title length
    if len(task_data.title) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title exceeds maximum length of 255 characters"
        )

    # Validate description length
    if task_data.description and len(task_data.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description exceeds maximum length of 1000 characters"
        )

    # Convert user_id to int for database operations
    user_id_int = int(user_id)
    # Enforce ownership at DB layer: create task for authenticated user
    task = TaskService.create_task(db, user_id_int, task_data.title, task_data.description)
    return task


@router.put("/{user_id}/tasks/{task_id}")
def update_task(user_id: str, task_id: int, task_data: TaskUpdate, db: Session = Depends(get_session), jwt_sub: str = Depends(get_current_user)):
    """
    Update specific task.
    Implements FR-005: Users MUST be able to update details of their existing tasks including title, description, and completion status
    Implements FR-009: System MUST enforce authentication for all API endpoints with valid JWT tokens
    Implements FR-010: System MUST ensure users can only access their own tasks
    Implements FR-003.1: System MUST return HTTP 400 Bad Request when task title exceeds 255 characters
    Implements FR-003.2: System MUST return HTTP 400 Bad Request when task description exceeds 1000 characters
    """
    # Enforce user isolation: path user_id must match JWT sub
    if jwt_sub != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only update your own tasks"
        )

    # Validate title length if provided
    if task_data.title and len(task_data.title) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title exceeds maximum length of 255 characters"
        )

    # Validate description length if provided
    if task_data.description and len(task_data.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description exceeds maximum length of 1000 characters"
        )

    # Convert user_id to int for database operations
    user_id_int = int(user_id)
    # Enforce ownership at DB layer: update task for authenticated user
    updated_task = TaskService.update_task(
        db, task_id, user_id_int,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    return updated_task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(user_id: str, task_id: int, db: Session = Depends(get_session), jwt_sub: str = Depends(get_current_user)):
    """
    Mark task as deleted (soft delete).
    Implements FR-006: Users MUST be able to delete their own tasks, with soft deletion (marked as deleted but retained for 30 days)
    Implements FR-006.1: Soft-deleted tasks MUST NOT appear in normal task list queries
    Implements FR-009: System MUST enforce authentication for all API endpoints with valid JWT tokens
    Implements FR-010: System MUST ensure users can only access their own tasks
    """
    # Enforce user isolation: path user_id must match JWT sub
    if jwt_sub != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only delete your own tasks"
        )

    # Convert user_id to int for database operations
    user_id_int = int(user_id)
    # Enforce ownership at DB layer: delete task for authenticated user
    success = TaskService.delete_task(db, task_id, user_id_int)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    return {"message": "Task marked as deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/toggle")
def toggle_task_completion(user_id: str, task_id: int, db: Session = Depends(get_session), jwt_sub: str = Depends(get_current_user)):
    """
    Toggle completion status.
    Implements FR-007: Users MUST be able to toggle the completion status of their tasks
    Implements FR-009: System MUST enforce authentication for all API endpoints with valid JWT tokens
    Implements FR-010: System MUST ensure users can only access their own tasks
    """
    # Enforce user isolation: path user_id must match JWT sub
    if jwt_sub != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only toggle completion status of your own tasks"
        )

    # Convert user_id to int for database operations
    user_id_int = int(user_id)
    # Enforce ownership at DB layer: toggle task for authenticated user
    task = TaskService.toggle_task_completion(db, task_id, user_id_int)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    return task


@router.get("/{user_id}/tasks/deleted")
def get_deleted_tasks(user_id: str, db: Session = Depends(get_session), jwt_sub: str = Depends(get_current_user)):
    """
    Retrieve soft-deleted tasks (admin endpoint).
    Implements FR-006.2: Soft-deleted tasks MUST be accessible via special endpoint with explicit permission
    Implements FR-009: System MUST enforce authentication for all API endpoints with valid JWT tokens
    Implements FR-010: System MUST ensure users can only access their own tasks
    """
    # Enforce user isolation: path user_id must match JWT sub
    if jwt_sub != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own deleted tasks"
        )

    # Convert user_id to int for database operations
    user_id_int = int(user_id)
    # Enforce ownership at DB layer: get deleted tasks for authenticated user
    deleted_tasks = TaskService.get_deleted_tasks_for_user(db, user_id_int)
    return deleted_tasks