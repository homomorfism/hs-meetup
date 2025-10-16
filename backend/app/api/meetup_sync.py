"""
API endpoints for syncing events from Meetup.com
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from ..database import get_db
from ..models import Event, Group, User
from ..services import meetup_api
from ..services.geocoding import geocode_event_location
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/meetup-sync", tags=["Meetup Sync"])


class SyncResult(BaseModel):
    success: bool
    imported_count: int
    skipped_count: int
    error_count: int
    errors: List[str] = []


class SyncRequest(BaseModel):
    keyword: str
    location: Optional[str] = None
    limit: int = 20
    create_group_if_missing: bool = True


@router.post("/search-and-import", response_model=SyncResult)
def search_and_import_events(
    sync_request: SyncRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search for events on Meetup and import them into our database.
    Requires authentication (admin users recommended).

    Args:
        keyword: Search keyword (e.g., "technology", "yoga")
        location: Optional location filter
        limit: Maximum number of events to import (default: 20)
        create_group_if_missing: Create groups automatically if they don't exist

    Returns:
        Summary of import operation
    """

    imported_count = 0
    skipped_count = 0
    error_count = 0
    errors = []

    try:
        # Fetch events from Meetup API
        print(f"Searching Meetup for events: keyword='{sync_request.keyword}', limit={sync_request.limit}")
        meetup_events = meetup_api.search_events_by_keyword(
            keyword=sync_request.keyword,
            location=sync_request.location,
            limit=sync_request.limit
        )

        if not meetup_events:
            return SyncResult(
                success=True,
                imported_count=0,
                skipped_count=0,
                error_count=0,
                errors=["No events found on Meetup for the given criteria"]
            )

        print(f"Found {len(meetup_events)} events from Meetup API")

        for meetup_event in meetup_events:
            try:
                # Check if event already exists (by meetup_id or title+date)
                meetup_id = meetup_event.get("meetup_id")
                existing_event = None

                if meetup_id:
                    # Check by external Meetup ID (we'll store this in description or a custom field)
                    existing_event = db.query(Event).filter(
                        Event.description.contains(f"meetup_id:{meetup_id}")
                    ).first()

                if existing_event:
                    print(f"Skipping duplicate event: {meetup_event['title']}")
                    skipped_count += 1
                    continue

                # Find or create group
                group_name = meetup_event.get("group_name", "Meetup Events")
                group = db.query(Group).filter(Group.name == group_name).first()

                if not group and sync_request.create_group_if_missing:
                    # Create new group for this Meetup group
                    group = Group(
                        name=group_name,
                        description=f"Events from Meetup.com - {group_name}",
                        category=meetup_event.get("category", "General"),
                        location=meetup_event.get("location_city", ""),
                        members_count=0,
                        organizer_id=current_user.id,  # Assign to current user
                        founded="2024-01-01 00:00:00"
                    )
                    db.add(group)
                    db.flush()  # Get the ID
                    print(f"Created new group: {group_name}")
                elif not group:
                    # Skip if group doesn't exist and we're not creating them
                    errors.append(f"Group '{group_name}' not found, skipping event: {meetup_event['title']}")
                    error_count += 1
                    continue

                # Geocode if coordinates not provided
                latitude = meetup_event.get("latitude")
                longitude = meetup_event.get("longitude")

                if not latitude or not longitude:
                    if not meetup_event.get("is_online"):
                        coords = geocode_event_location(
                            meetup_event.get("location", ""),
                            meetup_event.get("location_city", "")
                        )
                        if coords:
                            latitude, longitude = coords

                # Prepare description with Meetup metadata
                description = meetup_event.get("description", "")
                meetup_url = meetup_event.get("meetup_url", "")

                # Add metadata footer to description
                metadata = f"\n\n---\nImported from Meetup.com"
                if meetup_url:
                    metadata += f"\n[View on Meetup]({meetup_url})"
                if meetup_id:
                    metadata += f"\nmeetup_id:{meetup_id}"

                description = (description[:500] if description else "Event from Meetup.com") + metadata

                # Create event
                new_event = Event(
                    title=meetup_event["title"],
                    description=description,
                    date=meetup_event.get("date"),
                    time=meetup_event.get("time"),
                    location=meetup_event.get("location", ""),
                    location_city=meetup_event.get("location_city", ""),
                    is_online=meetup_event.get("is_online", False),
                    category=meetup_event.get("category", "General"),
                    image=meetup_event.get("image"),
                    price=str(meetup_event.get("price", 0.0)),
                    max_attendees=meetup_event.get("max_attendees"),
                    external_attendees_count=meetup_event.get("attendees_count", 0),
                    latitude=latitude,
                    longitude=longitude,
                    group_id=group.id,
                    organizer_id=current_user.id,
                )

                db.add(new_event)
                imported_count += 1
                print(f"Imported event: {new_event.title}")

            except Exception as e:
                error_msg = f"Error importing event '{meetup_event.get('title', 'Unknown')}': {str(e)}"
                print(error_msg)
                errors.append(error_msg)
                error_count += 1
                continue

        # Commit all changes
        db.commit()

        return SyncResult(
            success=True,
            imported_count=imported_count,
            skipped_count=skipped_count,
            error_count=error_count,
            errors=errors
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@router.post("/import-by-location", response_model=SyncResult)
def import_events_by_location(
    latitude: float = Query(..., description="Latitude coordinate"),
    longitude: float = Query(..., description="Longitude coordinate"),
    radius: int = Query(50, description="Search radius in miles"),
    limit: int = Query(20, description="Maximum events to import"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import events from Meetup near a specific location.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius: Search radius in miles (default: 50)
        limit: Maximum events to import (default: 20)

    Returns:
        Summary of import operation
    """

    imported_count = 0
    skipped_count = 0
    error_count = 0
    errors = []

    try:
        # Fetch events from Meetup API
        print(f"Searching Meetup for events near: lat={latitude}, lon={longitude}, radius={radius}")
        meetup_events = meetup_api.search_events_by_location(
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            limit=limit
        )

        if not meetup_events:
            return SyncResult(
                success=True,
                imported_count=0,
                skipped_count=0,
                error_count=0,
                errors=["No events found near this location"]
            )

        # Use same import logic as search_and_import_events
        # (Implementation would be similar to above)

        return SyncResult(
            success=True,
            imported_count=imported_count,
            skipped_count=skipped_count,
            error_count=error_count,
            errors=errors
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Location sync failed: {str(e)}")


@router.post("/import-by-geolocation")
def import_events_by_geolocation(
    latitude: float = Query(..., description="User's latitude"),
    longitude: float = Query(..., description="User's longitude"),
    limit: int = Query(50, description="Maximum events to import"),
    db: Session = Depends(get_db)
):
    """
    Import events from Meetup near user's current location.
    This endpoint is called automatically when user grants location permission.
    """

    imported_count = 0
    skipped_count = 0
    error_count = 0
    errors = []

    try:
        # Get first available user for imports (fallback to any user if admin doesn't exist)
        admin_user = db.query(User).filter(User.email == "admin@meetup.local").first()
        if not admin_user:
            # Use first available user as fallback
            admin_user = db.query(User).first()
            if not admin_user:
                raise HTTPException(status_code=500, detail="No users found in database")

        # Fetch events from Meetup API
        # Use broad search terms to get diverse events
        print(f"Auto-importing events near: lat={latitude}, lon={longitude}")
        all_meetup_events = []
        search_keywords = ["meetup", "networking", "social"]

        for keyword in search_keywords:
            events = meetup_api.search_events_by_location(
                latitude=latitude,
                longitude=longitude,
                radius=25,  # 25 mile radius around user
                limit=limit // len(search_keywords),
                keyword=keyword
            )
            all_meetup_events.extend(events)

        meetup_events = all_meetup_events

        if not meetup_events:
            return SyncResult(
                success=True,
                imported_count=0,
                skipped_count=0,
                error_count=0,
                errors=["No events found near your location"]
            )

        for meetup_event in meetup_events:
            try:
                # Check if event already exists
                meetup_id = meetup_event.get("meetup_id")
                if meetup_id:
                    existing_event = db.query(Event).filter(
                        Event.description.contains(f"meetup_id:{meetup_id}")
                    ).first()

                    if existing_event:
                        skipped_count += 1
                        continue

                # Find or create group
                group_name = meetup_event.get("group_name", "Local Events")
                group = db.query(Group).filter(Group.name == group_name).first()

                if not group:
                    # Fetch group details from Meetup API
                    group_urlname = meetup_event.get("group_urlname")
                    group_details = None
                    if group_urlname:
                        group_details = meetup_api.get_group_by_urlname(group_urlname)

                    group = Group(
                        name=group_name,
                        description=group_details.get("description", f"Events from {group_name}")[:500] if group_details else f"Events from {group_name}",
                        category=meetup_event.get("category", "General"),
                        location=group_details.get("location", meetup_event.get("location_city", "")) if group_details else meetup_event.get("location_city", ""),
                        members_count=group_details.get("members_count", 0) if group_details else 0,
                        image=group_details.get("image") if group_details else None,
                        organizer_id=admin_user.id,
                        founded="2024-01-01 00:00:00"
                    )
                    db.add(group)
                    db.flush()
                else:
                    # Update existing group with latest member count and image if not set
                    group_urlname = meetup_event.get("group_urlname")
                    if group_urlname and (not group.image or group.members_count == 0):
                        group_details = meetup_api.get_group_by_urlname(group_urlname)
                        if group_details:
                            if not group.image:
                                group.image = group_details.get("image")
                            if group.members_count == 0:
                                group.members_count = group_details.get("members_count", 0)
                            db.flush()

                # Geocode if needed
                event_latitude = meetup_event.get("latitude")
                event_longitude = meetup_event.get("longitude")

                if not event_latitude or not event_longitude:
                    if not meetup_event.get("is_online"):
                        coords = geocode_event_location(
                            meetup_event.get("location", ""),
                            meetup_event.get("location_city", "")
                        )
                        if coords:
                            event_latitude, event_longitude = coords
                        else:
                            # Use search location as fallback
                            event_latitude, event_longitude = latitude, longitude

                # Prepare description
                description = meetup_event.get("description", "")
                meetup_url = meetup_event.get("meetup_url", "")

                metadata = f"\\n\\n---\\nFrom Meetup.com"
                if meetup_url:
                    metadata += f"\\n[View on Meetup]({meetup_url})"
                if meetup_id:
                    metadata += f"\\nmeetup_id:{meetup_id}"

                description = (description[:500] if description else "Event from Meetup.com") + metadata

                # Create event
                new_event = Event(
                    title=meetup_event["title"],
                    description=description,
                    date=meetup_event.get("date"),
                    time=meetup_event.get("time"),
                    location=meetup_event.get("location", ""),
                    location_city=meetup_event.get("location_city", ""),
                    is_online=meetup_event.get("is_online", False),
                    category=meetup_event.get("category", "General"),
                    image=meetup_event.get("image"),
                    price=str(meetup_event.get("price", 0.0)),
                    max_attendees=meetup_event.get("max_attendees"),
                    external_attendees_count=meetup_event.get("attendees_count", 0),
                    latitude=event_latitude,
                    longitude=event_longitude,
                    group_id=group.id,
                    organizer_id=admin_user.id,
                )

                db.add(new_event)
                imported_count += 1

            except Exception as e:
                error_msg = f"Error importing event: {str(e)}"
                errors.append(error_msg)
                error_count += 1
                continue

        db.commit()

        return SyncResult(
            success=True,
            imported_count=imported_count,
            skipped_count=skipped_count,
            error_count=error_count,
            errors=errors
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.get("/test-connection")
def test_meetup_connection():
    """
    Test the Meetup API connection and authentication.
    Returns success if API key is valid.
    """
    try:
        # Try to fetch a single event as a test
        events = meetup_api.search_events_by_keyword(keyword="technology", limit=1)

        if events:
            return {
                "success": True,
                "message": "Meetup API connection successful",
                "sample_event": events[0].get("title") if events else None
            }
        else:
            return {
                "success": False,
                "message": "Connected to Meetup API but no events found. Check your API key permissions."
            }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")
