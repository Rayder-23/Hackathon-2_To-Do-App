"""
Initial database migration for Todo App Phase II
Creates all required tables based on SQLModel definitions
"""

from .session import engine
from sqlmodel import SQLModel
from ..models.user import User
from ..models.task import Task


def run_migrations():
    """
    Run the initial database migration to create all tables.
    """
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    run_migrations()