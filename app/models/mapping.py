from beanie import Document, Link
from typing import List
from models.menu_master import MenuMaster

class Mapping(Document):
    envKey: Link[Env]        # e.g. "dev", "prod"
    viewName: str      # e.g. "AdminDashboard"
    viewId: int
    menus: List[Link[MenuMaster]] # linked menus (which contain linked submenus)
    status: str  # active, inactive, draft ->default draft
    #func to mark_active

    class Settings:
        name = "mapping"
