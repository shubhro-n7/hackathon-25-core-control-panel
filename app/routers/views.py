from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from models.mapping import Mapping
from services.view_importer import sync_views_from_api

router = APIRouter()

@router.post("/views/sync", status_code=202)
async def trigger_sync(background_tasks: BackgroundTasks):
    """
    Triggers a background task to fetch all views from the source API
    and sync them to the MongoDB database.
    """
    background_tasks.add_task(sync_views_from_api)
    return {"message": "View synchronization started in the background."}


@router.get("/views", response_model=List[Mapping])
async def get_all_views():
    """
    Retrieve all view mappings from the local MongoDB database.
    """
    views = await Mapping.find_all(fetch_links=True).to_list()
    return views


@router.get("/views/{view_name}", response_model=Mapping)
async def get_view_by_name(view_name: str):
    """
    Retrieve a specific, active view mapping by its name.
    """
    view = await Mapping.find_one(
        Mapping.viewName == view_name,
        Mapping.status == "active",
        fetch_links=True
    )
    if view:
        return view
    raise HTTPException(status_code=404, detail=f"Active view '{view_name}' not found.")