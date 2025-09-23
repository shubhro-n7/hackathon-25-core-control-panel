"""
Database connection and initialization.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.config import settings
from app.models import Item


async def init_database():
    """Initialize database connection and Beanie ODM."""
    # Create Motor client
    client = AsyncIOMotorClient(settings.MONGO_URL)
    
    # Initialize Beanie with the Item document class and database
    await init_beanie(
        database=client[settings.DATABASE_NAME], 
        document_models=[Item]
    )
    
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")


async def close_database():
    """Close database connection (if needed for cleanup)."""
    # Motor handles connection pooling automatically
    # No explicit cleanup needed in most cases
    print("Database connection closed")