from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    category = Column(String, nullable=False, index=True)
    location = Column(String)
    members_count = Column(Integer, default=0)
    organizer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    image = Column(String)
    founded = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    organizer = relationship("User", back_populates="organized_groups", foreign_keys=[organizer_id])
    events = relationship("Event", back_populates="group", cascade="all, delete-orphan")
    members = relationship("User", secondary="group_members", back_populates="joined_groups")
