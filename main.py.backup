from fastapi import FastAPI, HTTPException
from beanie import Document, init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from datetime import datetime
from contextlib import asynccontextmanager

# MongoDB connection settings
MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:password123@mongodb:27017/fastapi_db?authSource=admin")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_db")

# Beanie Document Model
class Item(Document):
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

# Pydantic models for API requests/responses
class ItemCreate(BaseModel):
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
    id: PydanticObjectId = Field(..., alias="_id")
    name: str
    description: Optional[str]
    price: float
    created_at: datetime
    
    class Config:
        populate_by_name = True

# Database initialization
async def init_db():
    """Initialize database connection and Beanie ODM."""
    # Create Motor client
    client = AsyncIOMotorClient(MONGO_URL)
    
    # Initialize Beanie with the Item document class and database
    await init_beanie(database=client[DATABASE_NAME], document_models=[Item])

# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print("Database initialized successfully!")
    yield
    # Shutdown (cleanup if needed)
    print("Shutting down...")

# FastAPI app with lifespan events
app = FastAPI(
    title="FastAPI MongoDB Server with Beanie",
    version="2.0.0",
    description="A modern FastAPI application using Beanie ODM for MongoDB",
    lifespan=lifespan
)

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Welcome message."""
    return {"message": "FastAPI MongoDB Server with Beanie ODM is running!"}

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify database connection."""
    try:
        # Test database connection by counting documents
        count = await Item.count()
        return {
            "status": "healthy",
            "database": "connected",
            "total_items": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.post("/items/", response_model=Item, status_code=201, tags=["Items"])
async def create_item(item_data: ItemCreate):
    """Create a new item."""
    # Create a new Item document
    item = Item(**item_data.model_dump())
    
    # Save to database
    await item.insert()
    
    return item

@app.get("/items/", response_model=List[Item], tags=["Items"])
async def get_items(
    skip: int = 0, 
    limit: int = 10,
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """Get all items with optional filtering and pagination."""
    # Build query filters
    query = {}
    
    if name:
        query["name"] = {"$regex": name, "$options": "i"}  # Case-insensitive search
    
    if min_price is not None:
        query.setdefault("price", {})["$gte"] = min_price
        
    if max_price is not None:
        query.setdefault("price", {})["$lte"] = max_price
    
    # Execute query with pagination
    items = await Item.find(query).skip(skip).limit(limit).to_list()
    
    return items

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: PydanticObjectId):
    """Get a specific item by ID."""
    item = await Item.get(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(item_id: PydanticObjectId, item_update: ItemUpdate):
    """Update an existing item."""
    # Find the item
    item = await Item.get(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only provided fields
    update_data = item_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Update the item
    await item.update({"$set": update_data})
    
    # Return the updated item
    return await Item.get(item_id)

@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(item_id: PydanticObjectId):
    """Delete an item by ID."""
    item = await Item.get(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    await item.delete()
    
    return {"message": "Item deleted successfully"}

@app.get("/items/search/{search_term}", response_model=List[Item], tags=["Items"])
async def search_items(search_term: str, limit: int = 10):
    """Search items by name or description."""
    items = await Item.find({
        "$or": [
            {"name": {"$regex": search_term, "$options": "i"}},
            {"description": {"$regex": search_term, "$options": "i"}}
        ]
    }).limit(limit).to_list()
    
    return items

@app.get("/stats", tags=["Statistics"])
async def get_statistics():
    """Get database statistics."""
    total_items = await Item.count()
    avg_price = await Item.aggregate([
        {"$group": {"_id": None, "avg_price": {"$avg": "$price"}}}
    ]).to_list()
    
    avg_price_value = avg_price[0]["avg_price"] if avg_price else 0
    
    return {
        "total_items": total_items,
        "average_price": round(avg_price_value, 2) if avg_price_value else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
