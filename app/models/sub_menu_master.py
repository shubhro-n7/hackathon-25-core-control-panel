from beanie import Document
from typing import Optional

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
