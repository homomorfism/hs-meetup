from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SavedSearchBase(BaseModel):
    name: str
    keyword: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    is_online: Optional[bool] = None
    price: Optional[str] = None


class SavedSearchCreate(SavedSearchBase):
    pass


class SavedSearchUpdate(BaseModel):
    name: Optional[str] = None
    keyword: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    is_online: Optional[bool] = None
    price: Optional[str] = None


class SavedSearch(SavedSearchBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
