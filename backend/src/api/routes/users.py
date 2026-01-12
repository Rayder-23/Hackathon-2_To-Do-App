from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ...database.session import get_session
from ...models.user import UserCreate
from ...services.user_service import UserService
from ...services.auth_service import create_access_token
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/users/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_session)):
    """
    Register a new user.
    Implements FR-001: System MUST allow users to register with email and password credentials
    Implements FR-013: System MUST reject user registration attempts with duplicate email addresses and return HTTP 409 Conflict
    Implements FR-014: System MUST validate email format using the pattern /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    """
    try:
        user = UserService.create_user(db, user_data.email, user_data.password)

        # Create access token for the new user
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

        return {
            "id": user.id,
            "email": user.email,
            "jwt_token": access_token
        }
    except HTTPException as e:
        # Re-raise HTTP exceptions as they are (e.g., 400 for validation, 409 for conflict)
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/users/login")
def login_user(login_data: LoginRequest, db: Session = Depends(get_session)):
    """
    Authenticate user and return JWT.
    Implements FR-002: System MUST authenticate users via JWT tokens issued by Better Auth with expiration after 24 hours and refresh tokens valid for 7 days
    """
    user = UserService.authenticate_user(db, login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return {
        "jwt_token": access_token
    }