"""Configuration module for JWT verification with Better Auth."""

import os
from typing import Optional


class Config:
    """Configuration class for JWT verification settings."""

    # Secret key for JWT verification - should come from environment
    # This is the shared secret used by Better Auth to sign JWTs
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")

    # Algorithm used by Better Auth for JWT signing
    JWT_ALGORITHM: str = "HS256"

    # Clock skew tolerance for JWT expiration validation (in seconds)
    JWT_CLOCK_SKEW_TOLERANCE: int = 5

    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration values are set."""
        if not cls.BETTER_AUTH_SECRET:
            raise ValueError("BETTER_AUTH_SECRET environment variable must be set")
        return True