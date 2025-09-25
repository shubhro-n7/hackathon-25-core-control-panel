from beanie import Document, Link
from typing import List , Literal
from pydantic import BaseModel

from .menu_master import MenuMaster, SubMenuMaster
from .envs import Env

# --- Embedded SubMenu structure with visibility override ---
class SubMenuMapping(BaseModel):
    submenu: Link[SubMenuMaster]
    visible: bool = True   # default to true for this mapping

# --- Embedded Menu structure for mapping ---
class MenuMapping(BaseModel):
    menu: Link[MenuMaster]
    submenus: List[SubMenuMapping]

class Mapping(Document):
    env: Link[Env]        
    viewName: str      # e.g. "sme view"
    viewId: int
    menus: List[MenuMapping] # linked menus (which contain linked submenus)
    status: Literal["draft", "active", "inactive"] = "draft" # active, inactive, draft ->default draft
    #func to mark_active

    class Settings:
        name = "mapping"
    
    async def activate(self):
        """
        Marks this mapping as active.
        Ensures no other mapping with same env + viewId is active (they get marked inactive).
        """
        # Mark others inactive
        await Mapping.find(
            Mapping.env.id == self.env.id,
            Mapping.viewId == self.viewId,
            Mapping.status == "active",
            Mapping.id != self.id,
        ).update({"$set": {"status": "inactive"}})

        # Mark self active
        self.status = "active"
        await self.save()
