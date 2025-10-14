from pydantic import BaseModel
from datetime import datetime
from .user import User


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    conversation_id: int
    sender_id: int
    sent_at: datetime
    is_read: bool

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    pass


class ConversationCreate(BaseModel):
    friend_id: int


class Conversation(ConversationBase):
    id: int
    participant1_id: int
    participant2_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationWithDetails(Conversation):
    participant1: User
    participant2: User
    messages: list[Message] = []

    class Config:
        from_attributes = True
