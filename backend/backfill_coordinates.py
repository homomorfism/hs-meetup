#!/usr/bin/env python3
"""
Utility script to backfill latitude/longitude coordinates for existing events.
Run this script to automatically geocode all events that don't have coordinates yet.

Usage:
    python backfill_coordinates.py
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.models import Event
from app.services.geocoding import geocode_event_location
import time


def backfill_event_coordinates():
    """Geocode all events that don't have coordinates yet."""
    db = SessionLocal()

    try:
        # Find events without coordinates
        events_without_coords = db.query(Event).filter(
            (Event.latitude == None) | (Event.longitude == None),
            Event.is_online == False
        ).all()

        print(f"Found {len(events_without_coords)} events without coordinates")

        if not events_without_coords:
            print("No events need geocoding!")
            return

        updated_count = 0
        failed_count = 0

        for event in events_without_coords:
            print(f"\nProcessing event #{event.id}: {event.title}")
            print(f"  Location: {event.location}, {event.location_city}")

            coords = geocode_event_location(event.location, event.location_city or "")

            if coords:
                event.latitude = coords[0]
                event.longitude = coords[1]
                updated_count += 1
                print(f"  ✓ Geocoded: ({coords[0]}, {coords[1]})")
            else:
                failed_count += 1
                print(f"  ✗ Failed to geocode")

            # Be nice to the API - add a small delay
            time.sleep(0.2)

        # Commit all changes
        db.commit()

        print(f"\n{'='*60}")
        print(f"✅ Backfill complete!")
        print(f"   Updated: {updated_count} events")
        print(f"   Failed: {failed_count} events")
        print(f"{'='*60}")

    except Exception as e:
        print(f"Error during backfill: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    backfill_event_coordinates()
