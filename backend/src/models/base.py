from sqlmodel import SQLModel
from sqlalchemy.orm import declarative_base

# Base class for all models
Base = declarative_base()

class BaseModel(SQLModel):
    """
    Base model class that provides common functionality for all models
    """
    pass