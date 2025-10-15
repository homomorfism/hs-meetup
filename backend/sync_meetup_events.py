#!/usr/bin/env python3
"""
CLI script to sync events from Meetup.com

Usage:
    python sync_meetup_events.py --keyword "technology" --limit 50
    python sync_meetup_events.py --keyword "yoga" --location "San Francisco" --limit 20
"""

import argparse
import sys
from app.database import SessionLocal
from app.models import User
from app.services import meetup_api
from app.services.geocoding import geocode_event_location
from app.models import Event, Group


def get_or_create_default_user(db):
    """Get the first user or create a default one for importing events."""
    user = db.query(User).first()
    if not user:
        print("No users found. Please create a user first.")
        sys.exit(1)
    return user


def sync_events(keyword, location=None, limit=20):
    """
    Sync events from Meetup API to database.

    Args:
        keyword: Search keyword
        location: Optional location filter (city name or "lat,lon")
        limit: Maximum number of events to fetch
    """
    db = SessionLocal()

    try:
        # Get a user to assign as organizer
        user = get_or_create_default_user(db)
        print(f"Using user: {user.email} as event organizer")

        # Determine coordinates for search
        lat, lon = 37.7749, -122.4194  # Default to San Francisco

        if location:
            # Try to parse as "lat,lon"
            if ',' in location:
                try:
                    lat, lon = map(float, location.split(','))
                    print(f"Using coordinates: {lat}, {lon}")
                except ValueError:
                    # Not valid coordinates, try geocoding the location name
                    coords = geocode_event_location(location, "")
                    if coords:
                        lat, lon = coords
                        print(f"Geocoded '{location}' to: {lat}, {lon}")
                    else:
                        print(f"Warning: Could not geocode '{location}', using San Francisco")
            else:
                # Try geocoding as city name
                coords = geocode_event_location(location, "")
                if coords:
                    lat, lon = coords
                    print(f"Geocoded '{location}' to: {lat}, {lon}")
                else:
                    print(f"Warning: Could not geocode '{location}', using San Francisco")

        # Fetch events from Meetup
        print(f"\nSearching Meetup for: '{keyword}'" + (f" near {location}" if location else " (San Francisco area)"))
        print(f"Fetching up to {limit} events...")

        # Use keyword search with coordinates (eventSearch supports both keyword and location)
        # We'll temporarily modify the search function to accept lat/lon
        import requests
        from app.config import settings

        query = """
        query($query: String!, $lat: Float!, $lon: Float!, $radius: Float, $first: Int!) {
          eventSearch(
            filter: {
              query: $query,
              lat: $lat,
              lon: $lon,
              radius: $radius
            },
            first: $first
          ) {
            edges {
              node {
                id
                title
                description
                dateTime
                endTime
                duration
                eventUrl
                eventType
                maxTickets
                howToFindUs
                group {
                  id
                  name
                  urlname
                }
                featuredEventPhoto {
                  id
                  baseUrl
                }
                topics {
                  edges {
                    node {
                      id
                      name
                    }
                  }
                }
                rsvps {
                  totalCount
                }
              }
            }
          }
        }
        """

        variables = {
            "query": keyword,
            "lat": lat,
            "lon": lon,
            "radius": 50.0,
            "first": limit,
        }

        headers = {
            "Authorization": f"Bearer {settings.MEETUP_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            "https://api.meetup.com/gql-ext",
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=30
        )

        data = response.json()

        if "errors" in data:
            print(f"GraphQL errors: {data['errors']}")
            meetup_events = []
        else:
            edges = data.get("data", {}).get("eventSearch", {}).get("edges", [])
            meetup_events = []
            for edge in edges:
                event_data = edge.get("node", {})
                if event_data:
                    event = meetup_api.transform_meetup_event(event_data)
                    if event:
                        meetup_events.append(event)

        if not meetup_events:
            print("❌ No events found on Meetup")
            return

        print(f"✓ Found {len(meetup_events)} events from Meetup\n")

        imported_count = 0
        skipped_count = 0
        error_count = 0

        for idx, meetup_event in enumerate(meetup_events, 1):
            try:
                print(f"\n[{idx}/{len(meetup_events)}] Processing: {meetup_event['title'][:60]}...")

                # Check if event already exists
                meetup_id = meetup_event.get("meetup_id")
                if meetup_id:
                    existing = db.query(Event).filter(
                        Event.description.contains(f"meetup_id:{meetup_id}")
                    ).first()
                    if existing:
                        print(f"  ⊘ Skipped (already exists)")
                        skipped_count += 1
                        continue

                # Find or create group
                group_name = meetup_event.get("group_name", "Meetup Events")
                group = db.query(Group).filter(Group.name == group_name).first()

                if not group:
                    print(f"  → Creating group: {group_name}")
                    group = Group(
                        name=group_name,
                        description=f"Events from Meetup.com - {group_name}",
                        category=meetup_event.get("category", "General"),
                        location=meetup_event.get("location_city", ""),
                        members_count=0,
                        organizer_id=user.id,
                        founded="2024-01-01 00:00:00"
                    )
                    db.add(group)
                    db.flush()

                # Geocode if needed
                latitude = meetup_event.get("latitude")
                longitude = meetup_event.get("longitude")

                if not latitude or not longitude:
                    if not meetup_event.get("is_online"):
                        print(f"  → Geocoding location...")
                        coords = geocode_event_location(
                            meetup_event.get("location", ""),
                            meetup_event.get("location_city", "")
                        )
                        if coords:
                            latitude, longitude = coords
                            print(f"    Coordinates: {latitude}, {longitude}")

                # Prepare description with metadata
                description = meetup_event.get("description", "")
                meetup_url = meetup_event.get("meetup_url", "")

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
                    organizer_id=user.id,
                )

                db.add(new_event)
                imported_count += 1
                print(f"  ✓ Imported successfully")

            except Exception as e:
                print(f"  ✗ Error: {e}")
                error_count += 1
                continue

        # Commit all changes
        db.commit()

        print(f"\n{'='*60}")
        print(f"Sync completed!")
        print(f"  ✓ Imported: {imported_count}")
        print(f"  ⊘ Skipped:  {skipped_count}")
        print(f"  ✗ Errors:   {error_count}")
        print(f"{'='*60}\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Sync failed: {e}")
        sys.exit(1)

    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Sync events from Meetup.com to your database"
    )
    parser.add_argument(
        "--keyword",
        required=True,
        help="Search keyword (e.g., 'technology', 'yoga', 'hiking')"
    )
    parser.add_argument(
        "--location",
        help="Location to search (e.g., 'San Francisco, CA')"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of events to fetch (default: 20)"
    )

    args = parser.parse_args()

    print("="*60)
    print("Meetup Event Sync Tool")
    print("="*60)

    sync_events(
        keyword=args.keyword,
        location=args.location,
        limit=args.limit
    )


if __name__ == "__main__":
    main()
