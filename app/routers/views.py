# routes/views.py
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId

from app.models import Env, MenuMaster, View, SubMenuMaster

router = APIRouter(prefix="/views", tags=["Views"])


# ------------------------------
# Create a new View mapping
# ------------------------------
@router.post("/", response_model=dict)
async def create_view(view_data: dict):
    """
    Create a new View (mapping).
    Input example:
    {
        "envId": "<Env_id>",
        "viewName": "DEFAULT_VIEW",
        "menus": [
            {
                "menuId": "<MenuMaster_id>",
                "order": 1,
                "subMenus": [
                    {
                        "subMenuId": "<SubMenuMaster_id>",
                        "order": 1,
                        "visible": true
                    }
                ]
            }
        ]
    }
    """
    try:
        env = await Env.get(PydanticObjectId(view_data["envId"]))
        if not env:
            raise HTTPException(status_code=404, detail=f"Env {view_data['envId']} not found")

        # Validate that menuIds and subMenuIds exist
        for menu in view_data.get("menus", []):
            if not await MenuMaster.get(PydanticObjectId(menu["menuId"])):
                raise HTTPException(status_code=404, detail=f"MenuMaster {menu['menuId']} not found")

            for sm in menu.get("subMenus", []):
                if not await SubMenuMaster.get(PydanticObjectId(sm["subMenuId"])):
                    raise HTTPException(status_code=404, detail=f"SubMenuMaster {sm['subMenuId']} not found")

        view_data["env"] = env
        view_data.pop("envId")  # replace with Link

        view = View(**view_data)
        await view.insert()
        return {"id": str(view.id), "message": "View mapping created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------------------
# Get expanded View JSON
# ------------------------------
@router.get("/{view_id}", response_model=dict)
async def get_view(view_id: str):
    """
    Fetch and expand a view into full JSON format.
    """
    view_doc = await View.get_full_view(PydanticObjectId(view_id))
    if not view_doc:
        raise HTTPException(status_code=404, detail="View not found")
    return view_doc


# ------------------------------
# Activate a View
# ------------------------------
@router.put("/{view_id}/activate", response_model=dict)
async def activate_view(view_id: str):
    """
    Mark the given view as active, deactivate others
    with the same env and viewName.
    """
    view = await View.get(PydanticObjectId(view_id))
    if not view:
        raise HTTPException(status_code=404, detail="View not found")

    await view.set_active()
    return {"id": str(view.id), "status": view.status, "message": "View activated successfully"}
