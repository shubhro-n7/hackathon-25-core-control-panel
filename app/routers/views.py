# routes/views.py
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId

from app.models import Env, MenuMaster, View, SubMenuMaster

router = APIRouter(prefix="/views", tags=["Views"])


# ------------------------------
# Create a new View mapping
# ------------------------------
@router.post("/", response_model=dict)
async def create_view(data: dict):
    """
    Create a new View (mapping).
    Input example:
    {
        "envId": "68d4e753368c2bc162577889",
        "viewData": {
            "id": 1,
            "name": "DEFAULT_VIEW",
            "menus": [
                {
                    "id": 32492,
                    "menuId": 1,
                    "name": "OVERVIEW",
                    "label": "Overview",
                    "icon": null,
                    "order": 1,
                    "entities": [
                        {
                            "id": 32493,
                            "entityId": 19,
                            "name": "HOME",
                            "label": "Home",
                            "link": "new-home",
                            "order": 1,
                            "icon": "nav-icon fa fa-home",
                            "visible": true
                        }
                    ]
                },
                {
                    "id": 32496,
                    "menuId": 2,
                    "name": "INTELLIGENT_DIAGNOSTICS",
                    "label": "Intelligent Diagnostics",
                    "icon": "nav-icon fas fa-table",
                    "order": 2,
                    "entities": [
                        {
                            "id": 396595,
                            "entityId": 2,
                            "name": "SERVICE_REQUEST",
                            "label": "Service Request",
                            "link": "caseobject",
                            "order": 3,
                            "icon": "nav-icon fas fa-wrench",
                            "visible": true
                        }
                    ]
                }
            ]
        }
    }
    """
    try:
        env = await Env.get(PydanticObjectId(data["envId"]))
        if not env:
            raise HTTPException(status_code=404, detail=f"Env {data['envId']} not found")
        view_data = data["viewData"]
        if not view_data:
            raise HTTPException(status_code=400, detail="viewData is required")

        # Build menus for View model
        menus_for_view = []
        for menu in view_data.get("menus", []):
            # Find or create MenuMaster
            menu_master = await MenuMaster.find_one(MenuMaster.name == menu["name"])
            if not menu_master:
                menu_master = MenuMaster(name=menu["name"], label=menu.get("label", menu["name"]), icon=menu.get("icon"))
                await menu_master.insert()
            menu_id = menu_master.id

            # Build subMenus for ViewMenuMap
            sub_menus_for_view = []
            for sm in menu.get("entities", []):
                # Find or create SubMenuMaster
                sub_menu_master = await SubMenuMaster.find_one(SubMenuMaster.name == sm["name"])
                if not sub_menu_master:
                    sub_menu_master = SubMenuMaster(
                        name=sm["name"],
                        label=sm.get("label", sm["name"]),
                        link=sm.get("link"),
                        icon=sm.get("icon"),
                        visible=sm.get("visible", True)
                    )
                    await sub_menu_master.insert()
                sub_menu_id = sub_menu_master.id

                sub_menus_for_view.append({
                    "subMenuId": sub_menu_id,
                    "order": sm.get("order"),
                    "visible": sm.get("visible")
                })

            menus_for_view.append({
                "menuId": menu_id,
                "order": menu.get("order"),
                "subMenus": sub_menus_for_view
            })

        view_data_object = {
            "env": env,
            "id": view_data["id"],
            "name": view_data["name"],
            "menus": menus_for_view,
            "status": view_data.get("status", "draft")
        }

        view = View(**view_data_object)
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
