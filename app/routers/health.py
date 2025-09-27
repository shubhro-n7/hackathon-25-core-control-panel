"""
Health check and statistics API endpoints.
"""
from fastapi import APIRouter, HTTPException

from app.models import Item

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    """Welcome message."""
    return {"message": "FastAPI MongoDB Server with Beanie ODM is running!!!"}


@router.get("/health", tags=["Health"])
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
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection failed: {str(e)}"
        )


@router.get("/stats", tags=["Statistics"])
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