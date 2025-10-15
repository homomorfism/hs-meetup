#!/usr/bin/env python3
"""
Test script to explore Meetup API and see what's actually available
"""

import requests
import json
from app.config import settings

API_URL = "https://api.meetup.com/gql-ext"

# Introspection query to get the schema
introspection_query = """
query IntrospectionQuery {
  __schema {
    queryType {
      name
      fields {
        name
        description
      }
    }
  }
}
"""

# Simple test query
simple_query = """
{
  __type(name: "Query") {
    fields {
      name
      description
    }
  }
}
"""

headers = {
    "Authorization": f"Bearer {settings.MEETUP_API_KEY}",
    "Content-Type": "application/json",
}

print("="*60)
print("Testing Meetup API")
print("="*60)
print(f"API URL: {API_URL}")
print(f"API Key: {settings.MEETUP_API_KEY[:10]}..." if settings.MEETUP_API_KEY else "NOT SET")
print("="*60)

# Test 1: Introspection
print("\n[Test 1] Schema Introspection...")
try:
    response = requests.post(
        API_URL,
        json={"query": introspection_query},
        headers=headers,
        timeout=30
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")

# Test 2: Get available queries
print("\n[Test 2] Available Queries...")
try:
    response = requests.post(
        API_URL,
        json={"query": simple_query},
        headers=headers,
        timeout=30
    )
    print(f"Status: {response.status_code}")
    data = response.json()

    if "data" in data and "__type" in data["data"]:
        fields = data["data"]["__type"]["fields"]
        print("\nAvailable queries:")
        for field in fields[:20]:  # Show first 20
            print(f"  - {field['name']}: {field.get('description', 'No description')}")
    else:
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
