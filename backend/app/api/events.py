from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date
from ..database import get_db
from ..models import Event, User, Group
from ..schemas.event import Event as EventSchema, EventCreate, EventUpdate
from ..schemas.user import User as UserSchema
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/events", tags=["Events"])


def add_attendees_count(event):
    """Helper function to add computed attendees_count to event object"""
    event.attendees_count = len(event.attendees)
    return event


@router.get("/", response_model=List[EventSchema])
def list_events(
    skip: int = 0,
    limit: int = 100,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    category: Optional[str] = None,
    is_online: Optional[bool] = None,
    price: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event).options(joinedload(Event.attendees))

    if keyword:
        query = query.filter(
            (Event.title.ilike(f"%{keyword}%")) | (Event.description.ilike(f"%{keyword}%"))
        )

    if location:
        query = query.filter(Event.location_city.ilike(f"%{location}%"))

    if category:
        query = query.filter(Event.category == category)

    if is_online is not None:
        query = query.filter(Event.is_online == is_online)

    if price:
        if price.lower() == "free":
            query = query.filter(Event.price.ilike("free"))
        elif price.lower() == "paid":
            query = query.filter(~Event.price.ilike("free"))

    events = query.offset(skip).limit(limit).all()

    # Add computed attendees_count to each event
    for event in events:
        add_attendees_count(event)

    return events


@router.get("/{event_id}", response_model=EventSchema)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).options(joinedload(Event.attendees)).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    add_attendees_count(event)
    return event


@router.post("/", response_model=EventSchema, status_code=201)
def create_event(
    event: EventCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify group exists
    group = db.query(Group).filter(Group.id == event.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Verify user is organizer of the group
    if group.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only group organizers can create events")

    db_event = Event(**event.model_dump(), organizer_id=current_user.id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    add_attendees_count(db_event)
    return db_event


@router.put("/{event_id}", response_model=EventSchema)
def update_event(
    event_id: int,
    event_update: EventUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_event = db.query(Event).options(joinedload(Event.attendees)).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    if db_event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)

    db.commit()
    db.refresh(db_event)
    add_attendees_count(db_event)
    return db_event


@router.post("/{event_id}/attend")
def attend_event(
    event_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    event = db.query(Event).options(joinedload(Event.attendees)).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if event is full
    current_count = len(event.attendees)
    if event.max_attendees and current_count >= event.max_attendees:
        raise HTTPException(status_code=400, detail="Event is full")

    if current_user not in event.attendees:
        event.attendees.append(current_user)
        db.commit()

    return {"message": "Successfully registered for the event"}


@router.get("/{event_id}/attendees", response_model=List[UserSchema])
def get_event_attendees(event_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    attendees = event.attendees[skip:skip + limit]
    return attendees
