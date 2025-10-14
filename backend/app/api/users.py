from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..database import get_db
from ..models import User, Event, Group
from ..schemas.user import User as UserSchema, UserUpdate
from ..schemas.event import Event as EventSchema
from ..schemas.group import Group as GroupSchema
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


def add_attendees_count(event):
    """Helper function to add computed attendees_count to event object"""
    event.attendees_count = len(event.attendees)
    return event


@router.get("/", response_model=List[UserSchema])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{user_id}/events", response_model=List[EventSchema])
def get_user_events(user_id: int, db: Session = Depends(get_db)):
    """Get events organized by the user"""
    events = db.query(Event).options(joinedload(Event.attendees)).filter(Event.organizer_id == user_id).all()
    for event in events:
        add_attendees_count(event)
    return events


@router.get("/{user_id}/attending", response_model=List[EventSchema])
def get_user_attending_events(user_id: int, db: Session = Depends(get_db)):
    """Get events the user is attending"""
    user = db.query(User).options(joinedload(User.attended_events).joinedload(Event.attendees)).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for event in user.attended_events:
        add_attendees_count(event)

    return user.attended_events


@router.get("/{user_id}/groups", response_model=List[GroupSchema])
def get_user_groups(user_id: int, db: Session = Depends(get_db)):
    groups = db.query(Group).filter(Group.organizer_id == user_id).all()
    return groups


@router.get("/{user_id}/friends", response_model=List[UserSchema])
def get_user_friends(user_id: int, db: Session = Depends(get_db)):
    """Get user's friends list"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.friends


@router.post("/{user_id}/friends/{friend_id}", response_model=UserSchema)
def add_friend(
    user_id: int,
    friend_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a friend"""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if user_id == friend_id:
        raise HTTPException(status_code=400, detail="Cannot add yourself as friend")

    user = db.query(User).filter(User.id == user_id).first()
    friend = db.query(User).filter(User.id == friend_id).first()

    if not user or not friend:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if already friends
    if friend in user.friends:
        raise HTTPException(status_code=400, detail="Already friends")

    # Add friendship (bidirectional)
    user.friends.append(friend)
    friend.friends.append(user)
    db.commit()
    db.refresh(user)

    return friend


@router.delete("/{user_id}/friends/{friend_id}")
def remove_friend(
    user_id: int,
    friend_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove a friend"""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    user = db.query(User).filter(User.id == user_id).first()
    friend = db.query(User).filter(User.id == friend_id).first()

    if not user or not friend:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if they are friends
    if friend not in user.friends:
        raise HTTPException(status_code=400, detail="Not friends")

    # Remove friendship (bidirectional)
    user.friends.remove(friend)
    friend.friends.remove(user)
    db.commit()

    return {"message": "Friend removed successfully"}
