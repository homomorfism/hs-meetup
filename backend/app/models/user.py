from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


# Association table for user interests
user_interests = Table(
    'user_interests',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
)

# Association table for event attendees
event_attendees = Table(
    'event_attendees',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id', ondelete='CASCADE'), primary_key=True)
)

# Association table for group members
group_members = Table(
    'group_members',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True)
)

# Association table for friendships
friendships = Table(
    'friendships',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    bio = Column(String)
    location = Column(String)
    avatar = Column(String)
    member_since = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    interests = relationship("Category", secondary="user_interests", back_populates="interested_users")
    organized_groups = relationship("Group", back_populates="organizer", foreign_keys="Group.organizer_id", cascade="all, delete-orphan")
    organized_events = relationship("Event", back_populates="organizer", foreign_keys="Event.organizer_id", cascade="all, delete-orphan")
    attended_events = relationship("Event", secondary=event_attendees, back_populates="attendees")
    joined_groups = relationship("Group", secondary=group_members, back_populates="members")

    # Friendships - bidirectional relationship
    friends = relationship(
        "User",
        secondary=friendships,
        primaryjoin=(id == friendships.c.user_id),
        secondaryjoin=(id == friendships.c.friend_id),
        backref="friend_of"
    )

    # Saved searches
    saved_searches = relationship("SavedSearch", back_populates="user", cascade="all, delete-orphan")

    # Search history
    search_history = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")
