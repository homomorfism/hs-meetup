from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import List, Optional, Any


class UserBase(BaseModel):
    email: EmailStr
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar: Optional[str] = None


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        """Validate password is at least 4 characters long"""
        if len(v) < 4:
            raise ValueError('Password must be at least 4 characters long')
        return v


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

    @field_validator('interests', mode='before')
    @classmethod
    def convert_interests(cls, v: Any) -> List[str]:
        """Convert Category objects to category names"""
        if not v:
            return []
        # If v is already a list of strings, return it
        if isinstance(v, list) and all(isinstance(item, str) for item in v):
            return v
        # If v is a list of Category objects, extract names
        return [item.name if hasattr(item, 'name') else str(item) for item in v]

    class Config:
        from_attributes = True


class UserWithPassword(User):
    password_hash: str
