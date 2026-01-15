from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from passlib.context import CryptContext
import re

# Configure password context with proper bcrypt backend settings to avoid version lookup issues
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",
    bcrypt__min_rounds=12,
)

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)


class UserCreate(SQLModel):
    """Schema for creating a new user."""
    email: str
    password: str


class User(UserBase, table=True):
    """
    User model representing a registered user with authentication credentials.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    hashed_password: str = Field(nullable=False, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def verify_password(self, plain_password: str) -> bool:
        """Verify a plaintext password against the hashed password."""
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plaintext password."""
        return pwd_context.hash(password)

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    # Relationship to Tasks
    tasks: List["Task"] = Relationship(back_populates="user")

    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """Validate password strength (minimum 8 chars)."""
        return len(password) >= 8

    @staticmethod
    def validate_password_strength_strict(password: str) -> bool:
        """Validate password strength with strict requirements (minimum 8 chars with uppercase, lowercase, number, special char)."""
        if len(password) < 8:
            return False

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        return has_upper and has_lower and has_digit and has_special