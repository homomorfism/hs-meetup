from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    location: Optional[str] = None
    image: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    image: Optional[str] = None


class Group(GroupBase):
    id: int
    members_count: int
    organizer_id: int
    founded: datetime

    class Config:
        from_attributes = True
