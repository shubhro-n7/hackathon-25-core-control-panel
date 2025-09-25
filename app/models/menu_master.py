from beanie import Document, Link
from typing import List, Optional
from models.sub_menu_master import SubMenuMaster

class MenuMaster(Document):
    id: int
    menuId: int
    name: str
    label: str
    icon: str
    entities: Optional[List[Link[SubMenuMaster]]]  # reference to SubMenuMaster

    class Settings:
        name = "menuMaster"  # MongoDB collection name
