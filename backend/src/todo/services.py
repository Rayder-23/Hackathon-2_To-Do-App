"""
Todo Business Services

This module implements business logic and rules for task operations.
"""
from typing import List, Optional
from .repository import TaskRepository
from .models import Task


class TodoService:
    """
    Business service layer for todo operations.
    Implements the business logic and rules for task operations.
    """

    def __init__(self):
        """Initialize the service with a task repository."""
        self.repository = TaskRepository()

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task with validation.

        Args:
            title: Required non-empty title for the task
            description: Optional description for the task

        Returns:
            The created Task object with assigned ID

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        # The Task model itself handles validation of the title
        return self.repository.add_task(title, description)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self.repository.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in creation order.

        Returns:
            List of all Task objects in the order they were created
        """
        return self.repository.get_all_tasks()

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task with validation.

        Args:
            task_id: The ID of the task to update
            title: New title (optional, keeps existing if None)
            description: New description (optional, keeps existing if None)

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        # Validate title if it's being updated
        if title is not None and (not title or not title.strip()):
            raise ValueError("Task title must be non-empty")

        return self.repository.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        return self.repository.delete_task(task_id)

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        return self.repository.toggle_task_completion(task_id)