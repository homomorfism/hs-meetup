from pydantic import BaseModel, computed_field
from datetime import date
from typing import Optional


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    time: str
    duration: Optional[str] = None
    location: Optional[str] = None
    location_city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price: str = "Free"
    is_online: bool = False
    category: str
    image: Optional[str] = None
    max_attendees: Optional[int] = None


class EventCreate(EventBase):
    group_id: int


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    time: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    location_city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price: Optional[str] = None
    is_online: Optional[bool] = None
    category: Optional[str] = None
    image: Optional[str] = None
    max_attendees: Optional[int] = None


class Event(EventBase):
    id: int
    group_id: int
    organizer_id: int
    attendees_count: int = 0

    class Config:
        from_attributes = True
