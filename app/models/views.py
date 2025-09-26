from datetime import datetime
from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field
from bson import ObjectId

from .envs import Env

# ------------------------------
# SubMenuMaster model
# ------------------------------
class SubMenuMaster(Document):
    name: str
    label: str
    link: str
    icon: Optional[str]
    visible: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "subMenuMaster"  # collection name


# ------------------------------
# MenuMaster model
# ------------------------------
class MenuMaster(Document):
    name: str
    label: str
    icon: Optional[str]
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "menuMaster"

# ------------------------------
# Embedded mapping inside View
# ------------------------------
class ViewSubMenuMap(BaseModel):
    subMenuId: ObjectId  # reference to SubMenuMaster._id
    order: int
    visible: Optional[bool] = None  # mapping-level override


class ViewMenuMap(BaseModel):
    menuId: ObjectId  # reference to MenuMaster._id
    order: int
    subMenus: List[ViewSubMenuMap] = []


# ------------------------------
# View model (mapping)
# ------------------------------
class View(Document):
    env: Link[Env]
    viewName: str
    menus: List[ViewMenuMap] = []
    status: str = Field(default="draft", regex="^(draft|active|inactive)$")
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "views"

    # --------------------------
    # METHODS
    # --------------------------

    async def expand_full(self) -> dict:
        """
        Build the full JSON (view -> menus -> subMenus).
        - Mapping-level visible overrides SubMenuMaster.visible
        - Menus and subMenus are sorted by order
        """
        from copy import deepcopy

        view_data = {
            "id": str(self.id),
            "envId": str(self.env.id) if self.env else None,
            "name": self.viewName,
            "menus": []
        }

        for m in sorted(self.menus, key=lambda x: x.order):
            menu_doc = await MenuMaster.get(m.menuId)
            if not menu_doc:
                continue

            menu_data = deepcopy(menu_doc.dict())
            menu_data["id"] = str(menu_doc.id)
            menu_data["order"] = m.order
            menu_data["entities"] = []  # keep "entities" in JSON

            for sm in sorted(m.subMenus, key=lambda x: x.order):
                sub_menu_doc = await SubMenuMaster.get(sm.subMenuId)
                if not sub_menu_doc:
                    continue

                sub_menu_data = deepcopy(sub_menu_doc.dict())
                sub_menu_data["id"] = str(sub_menu_doc.id)
                sub_menu_data["order"] = sm.order

                # Override visibility if provided
                if sm.visible is not None:
                    sub_menu_data["visible"] = sm.visible

                menu_data["entities"].append(sub_menu_data)

            view_data["menus"].append(menu_data)

        return view_data

    @classmethod
    async def get_full_view(cls, view_id: ObjectId) -> Optional[dict]:
        """
        Helper to fetch a view by Mongo _id and expand it fully.
        """
        view_doc = await cls.get(view_id)
        if view_doc:
            return await view_doc.expand_full()
        return None

    async def set_active(self):
        """
        Mark this view as active, and deactivate any other view
        with the same env and viewName.
        """
        await View.find(
            (View.env.id == self.env.id) &
            (View.viewName == self.viewName) &
            (View.id != self.id) &
            (View.status == "active")
        ).update({"$set": {"status": "inactive"}})

        self.status = "active"
        await self.save()
