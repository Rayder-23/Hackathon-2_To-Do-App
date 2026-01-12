from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
from sqlmodel import Session
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel

# Import models to register them with SQLModel metadata
from ..models import user, task

Base = SQLModel.metadata

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection in FastAPI.
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def create_db_and_tables():
    """
    Create database tables based on models.
    """
    SQLModel.metadata.create_all(bind=engine)
