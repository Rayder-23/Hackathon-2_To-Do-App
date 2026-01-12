"""
Task Model

This module defines the Task data structure with validation.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with an auto-incremented integer ID,
    required non-empty title, optional description, and boolean completion status.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title must be non-empty")