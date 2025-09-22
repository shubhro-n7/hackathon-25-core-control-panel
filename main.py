from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List, Annotated
import os
from datetime import datetime

app = FastAPI(title="FastAPI MongoDB Server", version="1.0.0")

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:password123@mongodb:27017/fastapi_db?authSource=admin")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_db")

client = MongoClient(MONGO_URL)
db = client[DATABASE_NAME]
collection = db["items"]

# MongoDB ObjectId validation
def validate_object_id(v):
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str):
        if ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId format")
    raise ValueError("ObjectId must be a valid ObjectId or string")

# Type annotation for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]

class ItemModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)

@app.get("/")
async def root():
    return {"message": "FastAPI MongoDB Server is running!"}

@app.get("/health")
async def health_check():
    try:
        # Test MongoDB connection
        client.admin.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.post("/items/", response_model=ItemModel)
async def create_item(item: ItemCreate):
    item_dict = item.model_dump()
    item_dict["created_at"] = datetime.utcnow()
    
    result = collection.insert_one(item_dict)
    created_item = collection.find_one({"_id": result.inserted_id})
    
    return ItemModel(**created_item)

@app.get("/items/", response_model=List[ItemModel])
async def read_items(skip: int = 0, limit: int = 10):
    items = list(collection.find().skip(skip).limit(limit))
    return [ItemModel(**item) for item in items]

@app.get("/items/{item_id}", response_model=ItemModel)
async def read_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID")
    
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return ItemModel(**item)

@app.put("/items/{item_id}", response_model=ItemModel)
async def update_item(item_id: str, item_update: ItemUpdate):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID")
    
    update_data = {k: v for k, v in item_update.model_dump(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = collection.update_one(
        {"_id": ObjectId(item_id)}, 
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = collection.find_one({"_id": ObjectId(item_id)})
    return ItemModel(**updated_item)

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID")
    
    result = collection.delete_one({"_id": ObjectId(item_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)