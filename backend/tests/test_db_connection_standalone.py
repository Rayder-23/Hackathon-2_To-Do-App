import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

def test_database_connection():
    """Test if the database connection can be established."""
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("ERROR: DATABASE_URL environment variable not found!")
        print("Please make sure your .env file is set up correctly.")
        return False

    print(f"SUCCESS: Found DATABASE_URL in environment: {'yes' if database_url else 'no'}")
    print(f"Database URL (first 50 chars): {database_url[:50]}...")

    try:
        # Create an engine to test the connection
        engine = create_engine(database_url, echo=False)

        # Attempt to connect
        with engine.connect() as connection:
            # Execute a simple query to test the connection
            result = connection.execute(text("SELECT 1"))
            print("SUCCESS: Database connection successful!")
            print("SUCCESS: Simple query execution successful!")
            return True

    except SQLAlchemyError as e:
        print(f"ERROR: SQLAlchemy Error: {e}")
        return False
    except Exception as e:
        print(f"ERROR: General Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Database Connection...")
    print("=" * 50)

    success = test_database_connection()

    print("=" * 50)
    if success:
        print("SUCCESS: Database connection test PASSED!")
        print("The Neon PostgreSQL database connection is working correctly.")
    else:
        print("FAILURE: Database connection test FAILED!")
        print("Please check your DATABASE_URL in the .env file.")