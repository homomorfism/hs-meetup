from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String)
    date = Column(Date, nullable=False, index=True)
    time = Column(String)
    duration = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    organizer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    location = Column(String)
    location_city = Column(String, index=True)
    attendees_count = Column(Integer, default=0)
    max_attendees = Column(Integer, nullable=True)
    price = Column(String)
    is_online = Column(Boolean, default=False, index=True)
    category = Column(String, nullable=False, index=True)
    image = Column(String)

    # Relationships
    group = relationship("Group", back_populates="events")
    organizer = relationship("User", back_populates="organized_events", foreign_keys=[organizer_id])
    attendees = relationship("User", secondary="event_attendees", back_populates="attended_events")
