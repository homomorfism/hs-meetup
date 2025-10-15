"""
Meetup API integration service for fetching real event data.

This service uses Meetup's GraphQL API to fetch events and transform them
into our application's schema.
"""

import requests
from typing import Optional, List, Dict, Any
from datetime import datetime
from ..config import settings


MEETUP_API_URL = "https://api.meetup.com/gql-ext"


def get_headers() -> Dict[str, str]:
    """Get headers for Meetup API requests with authentication."""
    if not settings.MEETUP_API_KEY:
        raise ValueError("MEETUP_API_KEY is not configured")

    return {
        "Authorization": f"Bearer {settings.MEETUP_API_KEY}",
        "Content-Type": "application/json",
    }


def search_events_by_keyword(
    keyword: str,
    location: Optional[str] = None,
    limit: int = 20,
    radius: int = 50
) -> List[Dict[str, Any]]:
    """
    Search for events on Meetup using keyword and optional location.

    Args:
        keyword: Search term (e.g., "technology", "yoga", "hiking")
        location: City or location name (e.g., "San Francisco, CA")
        limit: Maximum number of events to return
        radius: Search radius in miles (default: 50)

    Returns:
        List of event dictionaries with transformed data
    """

    # GraphQL query to search for events
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

    # Default to San Francisco if no location specified (lat/lon are REQUIRED)
    lat = 37.7749
    lon = -122.4194

    variables = {
        "query": keyword,
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "first": limit,
    }

    try:
        response = requests.post(
            MEETUP_API_URL,
            json={"query": query, "variables": variables},
            headers=get_headers(),
            timeout=30
        )
        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            print(f"GraphQL errors: {data['errors']}")
            return []

        # Extract and transform events
        events = []
        edges = data.get("data", {}).get("eventSearch", {}).get("edges", [])

        for edge in edges:
            event_data = edge.get("node", {})
            if event_data:
                event = transform_meetup_event(event_data)
                if event:
                    events.append(event)

        return events

    except requests.exceptions.RequestException as e:
        print(f"Error fetching events from Meetup API: {e}")
        return []


def search_events_by_location(
    latitude: float,
    longitude: float,
    radius: int = 50,
    limit: int = 20,
    keyword: str = "meetup"
) -> List[Dict[str, Any]]:
    """
    Search for events near a specific location.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius: Search radius in miles
        limit: Maximum number of events to return
        keyword: Search keyword (default: "meetup" for broad results)

    Returns:
        List of event dictionaries
    """

    # Note: query parameter is REQUIRED by Meetup API, cannot be empty
    query = """
    query($lat: Float!, $lon: Float!, $radius: Float, $first: Int!, $query: String!) {
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
        "lat": latitude,
        "lon": longitude,
        "radius": float(radius),
        "first": limit,
        "query": keyword,
    }

    try:
        response = requests.post(
            MEETUP_API_URL,
            json={"query": query, "variables": variables},
            headers=get_headers(),
            timeout=30
        )
        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            print(f"GraphQL errors: {data['errors']}")
            return []

        events = []
        edges = data.get("data", {}).get("eventSearch", {}).get("edges", [])

        for edge in edges:
            event_data = edge.get("node", {})
            if event_data:
                event = transform_meetup_event(event_data)
                if event:
                    events.append(event)

        return events

    except requests.exceptions.RequestException as e:
        print(f"Error fetching events from Meetup API: {e}")
        return []


def transform_meetup_event(meetup_event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Transform a Meetup event into our application's event schema.

    Args:
        meetup_event: Raw event data from Meetup API

    Returns:
        Transformed event dictionary matching our schema, or None if invalid
    """
    try:
        # Extract venue information (no venue in the schema - we'll use howToFindUs)
        group = meetup_event.get("group", {})
        venue = None  # Venue not available in this schema

        # Determine if event is online
        event_type = meetup_event.get("eventType", "")
        is_online = event_type == "ONLINE" if event_type else False

        # Build location string (using howToFindUs since venue not available)
        if is_online:
            location = "Online Event"
            location_city = ""
        else:
            location = meetup_event.get("howToFindUs", "") or "Location TBD"
            location_city = ""

        # Coordinates not available in this response, will be geocoded later
        latitude = None
        longitude = None

        # Parse date/time
        date_time_str = meetup_event.get("dateTime", "")
        if date_time_str:
            # Parse ISO format datetime
            event_datetime = datetime.fromisoformat(date_time_str.replace("Z", "+00:00"))
            date = event_datetime.strftime("%Y-%m-%d")
            time = event_datetime.strftime("%H:%M")
        else:
            date = None
            time = None

        # Extract category from topics (topics is now a connection with edges)
        topics = meetup_event.get("topics", {}).get("edges", [])
        topic_names = [t.get("node", {}).get("name") for t in topics if t.get("node")]
        category = topic_names[0] if topic_names else "General"

        # Map category to our categories
        category_mapping = {
            "technology": "Technology",
            "tech": "Technology",
            "sports": "Sports & Fitness",
            "fitness": "Sports & Fitness",
            "arts": "Arts & Culture",
            "culture": "Arts & Culture",
            "food": "Food & Drink",
            "business": "Business & Professional",
            "career": "Business & Professional",
            "education": "Learning & Education",
            "music": "Music",
            "health": "Health & Wellness",
            "wellness": "Health & Wellness",
            "outdoors": "Outdoors & Adventure",
            "adventure": "Outdoors & Adventure",
        }

        category_lower = category.lower()
        for key, value in category_mapping.items():
            if key in category_lower:
                category = value
                break

        # Get photo URL - combine baseUrl + id
        photo = meetup_event.get("featuredEventPhoto")
        if photo and photo.get("id") and photo.get("baseUrl"):
            image_url = f"{photo['baseUrl']}{photo['id']}/highres/"
        else:
            image_url = None

        # Determine price (Meetup API doesn't always provide this directly)
        price = 0.0  # Default to free
        max_attendees = meetup_event.get("maxTickets")

        # Get attendee count from rsvps connection
        rsvps = meetup_event.get("rsvps", {})
        attendees_count = rsvps.get("totalCount", 0) if rsvps else 0

        return {
            "title": meetup_event.get("title", "Untitled Event"),
            "description": meetup_event.get("description", ""),
            "date": date,
            "time": time,
            "location": location,
            "location_city": location_city,
            "is_online": is_online,
            "category": category,
            "image": image_url,
            "price": price,
            "attendees_count": attendees_count,
            "max_attendees": max_attendees,
            "latitude": latitude,
            "longitude": longitude,
            "meetup_id": meetup_event.get("id"),
            "meetup_url": meetup_event.get("eventUrl"),
            "group_name": group.get("name"),
            "group_urlname": group.get("urlname"),
        }

    except Exception as e:
        print(f"Error transforming event: {e}")
        return None


def get_event_by_id(event_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a specific event by its Meetup ID.

    Args:
        event_id: Meetup event ID

    Returns:
        Transformed event dictionary or None
    """

    query = """
    query($eventId: ID!) {
      event(id: $eventId) {
        id
        title
        description
        dateTime
        duration
        eventUrl
        eventType
        going
        maxTickets
        venue {
          name
          address
          city
          state
          country
          lat
          lng
        }
        group {
          id
          name
          urlname
          city
          state
        }
        featuredEventPhoto {
          baseUrl
        }
        topics {
          name
        }
      }
    }
    """

    variables = {"eventId": event_id}

    try:
        response = requests.post(
            MEETUP_API_URL,
            json={"query": query, "variables": variables},
            headers=get_headers(),
            timeout=30
        )
        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            print(f"GraphQL errors: {data['errors']}")
            return None

        event_data = data.get("data", {}).get("event")
        if event_data:
            return transform_meetup_event(event_data)

        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching event from Meetup API: {e}")
        return None
