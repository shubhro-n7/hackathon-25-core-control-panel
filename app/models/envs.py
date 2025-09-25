from datetime import datetime
from typing import Optional
from beanie import Document, Link
from pydantic import Field
from passlib.hash import bcrypt
import secrets


# ---------------------------
# Env Collection
# ---------------------------
class Env(Document):
    envName: str
    slug: str = Field(unique=True)  # useful for fast lookup
    description: Optional[str]
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: str

    class Settings:
        name = "envs"  # Mongo collection name


# ---------------------------
# EnvKey Collection
# ---------------------------
class EnvKey(Document):
    envId: Link[Env]
    hashedSecret: str
    status: str = Field(default="active")  # active | inactive | revoked
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    createdBy: str

    class Settings:
        name = "envKeys"

    # -----------------------
    # Secret management utils
    # -----------------------

    @staticmethod
    def generate_secret(length: int = 32) -> str:
        """Generate a cryptographically secure random secret (URL safe)."""
        return secrets.token_urlsafe(length)

    @staticmethod
    def hash_secret(secret: str) -> str:
        """Hash a secret using bcrypt."""
        return bcrypt.hash(secret)

    @staticmethod
    def verify_secret(secret: str, hashed: str) -> bool:
        """Verify secret against stored hash."""
        return bcrypt.verify(secret, hashed)
