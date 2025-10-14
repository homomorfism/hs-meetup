from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    participant1_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    participant2_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    participant1 = relationship("User", foreign_keys=[participant1_id])
    participant2 = relationship("User", foreign_keys=[participant2_id])
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.sent_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    is_read = Column(Boolean, default=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User")
