"""
Item document model using Beanie ODM.
"""
from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class Item(Document):
    """Item document model."""
    
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "items"  # Collection name
        
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sample Item",
                "description": "This is a sample item",
                "price": 29.99
            }
        }