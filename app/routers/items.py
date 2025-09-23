"""
Item CRUD API endpoints.
"""
from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from app.models import Item
from app.schemas import ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=Item, status_code=201)
async def create_item(item_data: ItemCreate):
    """Create a new item."""
    # Create a new Item document
    item = Item(**item_data.model_dump())
    
    # Save to database
    await item.insert()
    
    return item


@router.get("/", response_model=List[Item])
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


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: PydanticObjectId):
    """Get a specific item by ID."""
    item = await Item.get(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item


@router.put("/{item_id}", response_model=Item)
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


@router.delete("/{item_id}")
async def delete_item(item_id: PydanticObjectId):
    """Delete an item by ID."""
    item = await Item.get(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    await item.delete()
    
    return {"message": "Item deleted successfully"}


@router.get("/search/{search_term}", response_model=List[Item])
async def search_items(search_term: str, limit: int = 10):
    """Search items by name or description."""
    items = await Item.find({
        "$or": [
            {"name": {"$regex": search_term, "$options": "i"}},
            {"description": {"$regex": search_term, "$options": "i"}}
        ]
    }).limit(limit).to_list()
    
    return items