from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Event, Group
from ..schemas.user import User as UserSchema, UserUpdate
from ..schemas.event import Event as EventSchema
from ..schemas.group import Group as GroupSchema
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


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
    events = db.query(Event).filter(Event.organizer_id == user_id).all()
    return events


@router.get("/{user_id}/groups", response_model=List[GroupSchema])
def get_user_groups(user_id: int, db: Session = Depends(get_db)):
    groups = db.query(Group).filter(Group.organizer_id == user_id).all()
    return groups
