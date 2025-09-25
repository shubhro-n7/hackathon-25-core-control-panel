from beanie import Document, Link
from typing import List, Optional

class SubMenuMaster(Document):
    id: int
    entityId: int
    name: str
    label: str
    link: str
    icon: str
    visible: bool

    class Settings:
        name = "subMenuMaster"

class MenuMaster(Document):
    id: int
    menuId: int
    name: str
    label: str
    icon: str
    entities: Optional[List[Link[SubMenuMaster]]]  # reference to SubMenuMaster

    class Settings:
        name = "menuMaster"  # MongoDB collection name
