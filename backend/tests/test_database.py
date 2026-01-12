import sys
import os

# Add the backend directory to the path so we can import modules properly
backend_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, backend_dir)

# Add the src directory to the path so we can import our modules
src_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
sys.path.insert(0, src_dir)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from sqlmodel import Session, select
from src.database.session import engine
from src.models.user import User
from src.models.task import Task

def test_database_connection():
    """Test that we can connect to the database and perform basic operations."""
    try:
        # Try to create a session and execute a simple query
        with Session(engine) as session:
            # Execute a simple query to test the connection
            result = session.exec(select(User).limit(1))
            # The query should execute without throwing an exception
            assert result is not None
        print("Database connection test passed!")
    except Exception as e:
        print(f"Database connection test failed: {e}")
        raise

def test_user_model_creation():
    """Test that we can create and save a user model."""
    try:
        with Session(engine) as session:
            # Create a test user
            test_user = User(
                email="test@example.com",
                hashed_password="hashed_test_password"
            )

            # Add to session and commit
            session.add(test_user)
            session.commit()

            # Refresh to get the auto-generated ID
            session.refresh(test_user)

            # Verify the user was created
            assert test_user.id is not None
            assert test_user.email == "test@example.com"

            # Clean up: delete the test user
            session.delete(test_user)
            session.commit()

        print("User model creation test passed!")
    except Exception as e:
        print(f"User model creation test failed: {e}")
        raise

def test_task_model_creation():
    """Test that we can create and save a task model."""
    try:
        with Session(engine) as session:
            # First create a test user (since task has a user relationship)
            test_user = User(
                email="task_test@example.com",
                hashed_password="hashed_test_password"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)

            # Now create a test task
            test_task = Task(
                title="Test Task",
                description="This is a test task",
                completed=False,
                user_id=test_user.id
            )

            # Add to session and commit
            session.add(test_task)
            session.commit()

            # Refresh to get the auto-generated ID
            session.refresh(test_task)

            # Verify the task was created
            assert test_task.id is not None
            assert test_task.title == "Test Task"
            assert test_task.user_id == test_user.id

            # Clean up: delete the task and user
            session.delete(test_task)
            session.delete(test_user)
            session.commit()

        print("Task model creation test passed!")
    except Exception as e:
        print(f"Task model creation test failed: {e}")
        raise

if __name__ == "__main__":
    test_database_connection()
    test_user_model_creation()
    test_task_model_creation()
    print("\nAll database tests passed!")