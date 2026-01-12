from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import users, tasks
from .database.session import create_db_and_tables
from .models.base import Base
from .database.session import engine
from sqlmodel import Session
from .api.middleware.rate_limit_middleware import RateLimitMiddleware
import os

# Create the FastAPI app
app = FastAPI(
    title="Todo App API",
    description="API for the Todo Application Phase II with BetterAuth integration",
    version="1.0.0"
)

# Add CORS middleware
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001")
allowed_origins = allowed_origins_str.split(",") if allowed_origins_str else ["*"]

# Add rate limiting middleware first
app.add_middleware(RateLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header to frontend for BetterAuth integration
    expose_headers=["Authorization", "Set-Cookie"]
)

# Include API routes
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    create_db_and_tables()

@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {"message": "Todo App API is running!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "todo-api", "database": "connected"}

# Dependency for database session
def get_db():
    with Session(engine) as session:
        yield session