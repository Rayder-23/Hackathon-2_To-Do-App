"""
In-Memory Task Repository

This module manages in-memory storage of tasks with CRUD operations.
"""
from typing import Dict, List, Optional
from .models import Task


class TaskRepository:
    """
    In-memory repository for managing tasks using a dictionary for O(1) lookup
    and a list to maintain creation order. Includes an ID counter for auto-incrementing IDs.
    """

    def __init__(self):
        """Initialize the repository with empty storage and ID counter."""
        self._tasks: Dict[int, Task] = {}
        self._task_list: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task with the given title and optional description.

        Args:
            title: Required non-empty title for the task
            description: Optional description for the task

        Returns:
            The created Task object with assigned ID
        """
        # Create the task with the current next ID
        task = Task(id=self._next_id, title=title, description=description, completed=False)

        # Store the task in both dictionary and list
        self._tasks[task.id] = task
        self._task_list.append(task)

        # Increment the ID counter for the next task
        self._next_id += 1

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in creation order.

        Returns:
            List of all Task objects in the order they were created
        """
        return self._task_list.copy()

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task with new values.

        Args:
            task_id: The ID of the task to update
            title: New title (optional, keeps existing if None)
            description: New description (optional, keeps existing if None)

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        if task_id not in self._tasks:
            return False

        # Remove from dictionary
        task = self._tasks.pop(task_id)

        # Remove from list while preserving order
        self._task_list.remove(task)

        return True

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]
        task.completed = not task.completed

        return task