from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar: Optional[str] = None


class User(UserBase):
    id: int
    member_since: datetime
    is_active: bool
    interests: List[str] = []

    class Config:
        from_attributes = True


class UserWithPassword(User):
    password_hash: str
