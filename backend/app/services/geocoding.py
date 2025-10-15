"""
Geocoding service to convert addresses to latitude/longitude coordinates
Uses Google Maps Geocoding API
"""
import os
import requests
from typing import Optional, Tuple


GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")


def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert an address string to latitude/longitude coordinates.

    Args:
        address: Full address string (e.g., "123 Main St, San Francisco, CA")

    Returns:
        Tuple of (latitude, longitude) or None if geocoding fails
    """
    if not address or not GOOGLE_MAPS_API_KEY:
        return None

    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": GOOGLE_MAPS_API_KEY
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        if data["status"] == "OK" and len(data["results"]) > 0:
            location = data["results"][0]["geometry"]["location"]
            return (location["lat"], location["lng"])
        else:
            print(f"Geocoding failed for address: {address}. Status: {data.get('status')}")
            return None

    except Exception as e:
        print(f"Error geocoding address '{address}': {e}")
        return None


def geocode_event_location(location: str, location_city: str) -> Optional[Tuple[float, float]]:
    """
    Geocode an event location. Tries full location first, falls back to city.

    Args:
        location: Venue address (e.g., "TechHub San Francisco, 123 Mission St")
        location_city: City and state (e.g., "San Francisco, CA")

    Returns:
        Tuple of (latitude, longitude) or None if geocoding fails
    """
    # Try full location first
    if location:
        full_address = f"{location}, {location_city}" if location_city else location
        coords = geocode_address(full_address)
        if coords:
            return coords

    # Fall back to city only
    if location_city:
        return geocode_address(location_city)

    return None
