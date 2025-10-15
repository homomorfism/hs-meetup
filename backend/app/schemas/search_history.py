from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SearchHistoryBase(BaseModel):
    keyword: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    is_online: Optional[bool] = None
    price: Optional[str] = None


class SearchHistoryCreate(SearchHistoryBase):
    pass


class SearchHistory(SearchHistoryBase):
    id: int
    user_id: int
    searched_at: datetime

    class Config:
        from_attributes = True
