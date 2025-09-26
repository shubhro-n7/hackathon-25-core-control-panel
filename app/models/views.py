from datetime import datetime
from typing import List, Optional
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Literal

from .envs import Env
from pymongo import IndexModel, ASCENDING

# ------------------------------
# SubMenuMaster model
# ------------------------------
class SubMenuMaster(Document):
    name: str = Field(unique=True)
    label: str
    link: str
    icon: Optional[str]
    visible: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "subMenuMaster"  # collection name
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True)
        ]


# ------------------------------
# MenuMaster model
# ------------------------------
class MenuMaster(Document):
    name: str = Field(unique=True)
    label: str
    icon: Optional[str]
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "menuMaster"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True)
        ]

# ------------------------------
# Embedded mapping inside View
# ------------------------------
class ViewSubMenuMap(BaseModel):
    subMenuId: PydanticObjectId  # reference to SubMenuMaster._id
    order: Optional[int] = None
    visible: Optional[bool] = None  # mapping-level override


class ViewMenuMap(BaseModel):
    menuId: PydanticObjectId  # reference to MenuMaster._id
    order: Optional[int] = None
    subMenus: List[ViewSubMenuMap] = []


# ------------------------------
# View model (mapping)
# ------------------------------
class View(Document):
    env: Link[Env]
    viewId: int
    name: str
    menus: List[ViewMenuMap] = []
    status: Literal["draft", "active", "inactive"] = "draft"
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "view"

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
            "id": str(self.viewId),
            "name": self.name,
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
    async def get_full_view(cls, view_id: PydanticObjectId) -> Optional[dict]:
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
        with the same env and name.
        """
        await View.find({
            "env": self.env,
            "name": self.name,
            "status": "active",
            "_id": {"$ne": self.id}
        }).update({"$set": {"status": "inactive"}})

        self.status = "active"
        await self.save()
