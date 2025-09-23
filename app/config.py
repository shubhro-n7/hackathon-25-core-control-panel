"""
Application configuration settings.
"""
import os
from typing import Optional


class Settings:
    """Application settings."""
    
    # MongoDB settings
    MONGO_URL: str = os.getenv(
        "MONGO_URL", 
        "mongodb://admin:password123@mongodb:27017/fastapi_db?authSource=admin"
    )
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "fastapi_db")
    
    # API settings
    API_TITLE: str = "FastAPI MongoDB Server with Beanie ODM"
    API_VERSION: str = "2.0.0"
    API_DESCRIPTION: str = "A modern FastAPI application using Beanie ODM for MongoDB"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"


# Global settings instance
settings = Settings()