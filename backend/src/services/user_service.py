from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from ..models.user import User
from fastapi import HTTPException, status

class UserService:
    """Service class for handling user-related operations."""

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get a user by email."""
        return db.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def create_user(db: Session, email: str, password: str) -> User:
        """Create a new user."""
        try:
            # Validate email format per FR-014
            if not User.validate_email(email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email format"
                )

            # Validate password strength (minimum 8 characters)
            if not User.validate_password_strength(password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password must be at least 8 characters long"
                )

            # Check if user already exists per FR-013
            existing_user = UserService.get_user_by_email(db, email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A user with this email already exists"
                )

            # Hash the password
            hashed_password = User.hash_password(password)

            # Create the user
            db_user = User(
                email=email,
                hashed_password=hashed_password,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            return db_user
        except HTTPException:
            # Re-raise HTTP exceptions as they are
            raise
        except Exception as e:
            # Log the error for debugging
            print(f"Error in create_user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred during user creation: {str(e)}"
            )

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = UserService.get_user_by_email(db, email)
        if not user or not user.verify_password(password):
            return None
        return user