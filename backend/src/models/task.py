from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
import re

class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a todo item belonging to a specific user.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relationship to User
    user: "User" = Relationship(back_populates="tasks")

    @classmethod
    def validate_title(cls, title: str) -> bool:
        """Validate task title length (1-255 characters)."""
        return 1 <= len(title) <= 255

    @classmethod
    def validate_description(cls, description: Optional[str]) -> bool:
        """Validate task description length (0-1000 characters)."""
        if description is None:
            return True
        return 0 <= len(description) <= 1000

    def soft_delete(self):
        """Mark task as deleted by setting deleted_at timestamp."""
        self.deleted_at = datetime.utcnow()
        return self