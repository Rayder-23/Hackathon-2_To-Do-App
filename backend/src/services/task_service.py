from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from ..models.task import Task
from ..models.user import User
from fastapi import HTTPException, status


class TaskService:
    """Service class for handling task-related operations."""

    @staticmethod
    def get_tasks_for_user(db: Session, user_id: int, include_deleted: bool = False) -> List[Task]:
        """Get all tasks for a specific user."""
        query = select(Task).where(Task.user_id == user_id)

        if not include_deleted:
            query = query.where(Task.deleted_at.is_(None))

        # Order by creation date, most recent first
        query = query.order_by(Task.created_at.desc())

        return db.exec(query).all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int, user_id: int, include_deleted: bool = False) -> Optional[Task]:
        """Get a specific task by ID for a specific user."""
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)

        if not include_deleted:
            query = query.where(Task.deleted_at.is_(None))

        return db.exec(query).first()

    @staticmethod
    def create_task(db: Session, user_id: int, title: str, description: Optional[str] = None) -> Task:
        """Create a new task for a user."""
        # Validate title
        if not Task.validate_title(title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Title must be between 1 and 255 characters"
            )

        # Validate description
        if not Task.validate_description(description):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be between 0 and 1000 characters"
            )

        # Create the task
        db_task = Task(
            title=title,
            description=description,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return db_task

    @staticmethod
    def update_task(db: Session, task_id: int, user_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Task]:
        """Update a task for a user."""
        db_task = TaskService.get_task_by_id(db, task_id, user_id)
        if not db_task:
            return None

        # Validate title if provided
        if title is not None:
            if not Task.validate_title(title):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title must be between 1 and 255 characters"
                )
            db_task.title = title

        # Validate description if provided
        if description is not None:
            if not Task.validate_description(description):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Description must be between 0 and 1000 characters"
                )
            db_task.description = description

        # Update completion status if provided
        if completed is not None:
            db_task.completed = completed

        # Update the timestamp
        db_task.updated_at = datetime.utcnow()

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: int) -> bool:
        """Soft delete a task for a user."""
        db_task = TaskService.get_task_by_id(db, task_id, user_id)
        if not db_task:
            return False

        # Mark as deleted (soft delete)
        db_task.soft_delete()
        db.add(db_task)
        db.commit()

        return True

    @staticmethod
    def toggle_task_completion(db: Session, task_id: int, user_id: int) -> Optional[Task]:
        """Toggle the completion status of a task."""
        db_task = TaskService.get_task_by_id(db, task_id, user_id)
        if not db_task:
            return None

        # Toggle completion status
        db_task.completed = not db_task.completed
        db_task.updated_at = datetime.utcnow()

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return db_task

    @staticmethod
    def get_deleted_tasks_for_user(db: Session, user_id: int) -> List[Task]:
        """Get soft-deleted tasks for a specific user."""
        query = select(Task).where(
            Task.user_id == user_id,
            Task.deleted_at.isnot(None)
        ).order_by(Task.created_at.desc())

        return db.exec(query).all()