from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Group, Event, User
from ..schemas.group import Group as GroupSchema, GroupCreate, GroupUpdate
from ..schemas.event import Event as EventSchema
from ..schemas.user import User as UserSchema
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/", response_model=List[GroupSchema])
def list_groups(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    location: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Group)

    if category:
        query = query.filter(Group.category == category)
    if location:
        query = query.filter(Group.location.ilike(f"%{location}%"))
    if keyword:
        # Search in both name and description
        search_filter = f"%{keyword}%"
        query = query.filter(
            (Group.name.ilike(search_filter)) | (Group.description.ilike(search_filter))
        )

    groups = query.offset(skip).limit(limit).all()
    return groups


@router.get("/{group_id}", response_model=GroupSchema)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.post("/", response_model=GroupSchema, status_code=201)
def create_group(
    group: GroupCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_group = Group(**group.model_dump(), organizer_id=current_user.id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


@router.put("/{group_id}", response_model=GroupSchema)
def update_group(
    group_id: int,
    group_update: GroupUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")

    if db_group.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = group_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_group, field, value)

    db.commit()
    db.refresh(db_group)
    return db_group


@router.post("/{group_id}/join")
def join_group(
    group_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if current_user not in group.members:
        group.members.append(current_user)
        group.members_count += 1
        db.commit()

    return {"message": "Successfully joined the group"}


@router.get("/{group_id}/events", response_model=List[EventSchema])
def get_group_events(group_id: int, db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.group_id == group_id).all()
    return events


@router.get("/{group_id}/members", response_model=List[UserSchema])
def get_group_members(group_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    members = group.members[skip:skip + limit]
    return members
