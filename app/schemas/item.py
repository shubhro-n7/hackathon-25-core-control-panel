"""
Pydantic schemas for Item API requests and responses.
"""
from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Schema for creating a new item."""
    
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sample Item",
                "description": "This is a sample item",
                "price": 29.99
            }
        }


class ItemUpdate(BaseModel):
    """Schema for updating an existing item."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Item",
                "description": "Updated description",
                "price": 39.99
            }
        }


class ItemResponse(BaseModel):
    """Schema for item responses."""
    
    id: PydanticObjectId = Field(..., alias="_id")
    name: str
    description: Optional[str]
    price: float
    created_at: datetime
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "Sample Item",
                "description": "This is a sample item",
                "price": 29.99,
                "created_at": "2023-06-15T10:30:00"
            }
        }