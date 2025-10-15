#!/usr/bin/env python3
"""
Explore the exact Meetup Event schema
"""

import requests
import json
from app.config import settings

API_URL = "https://api.meetup.com/gql-ext"

# Query to get Event type fields
event_schema_query = """
{
  __type(name: "Event") {
    fields {
      name
      type {
        name
        kind
      }
      description
    }
  }
}
"""

# Query to get eventSearch arguments
event_search_query = """
{
  __type(name: "Query") {
    fields(includeDeprecated: true) {
      name
      args {
        name
        type {
          name
          kind
          ofType {
            name
          }
        }
      }
    }
  }
}
"""

headers = {
    "Authorization": f"Bearer {settings.MEETUP_API_KEY}",
    "Content-Type": "application/json",
}

print("="*60)
print("Exploring Meetup Event Schema")
print("="*60)

# Get Event fields
print("\n[1] Event Type Fields:")
print("-"*60)
try:
    response = requests.post(
        API_URL,
        json={"query": event_schema_query},
        headers=headers,
        timeout=30
    )
    data = response.json()

    if "data" in data and "__type" in data["data"] and data["data"]["__type"]:
        fields = data["data"]["__type"]["fields"]
        print(f"Total fields: {len(fields)}\n")
        for field in fields[:40]:  # Show first 40
            print(f"  {field['name']}: {field['type'].get('name', field['type'].get('kind'))}")
    else:
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")

# Get eventSearch details
print("\n[2] Query.eventSearch Arguments:")
print("-"*60)
try:
    response = requests.post(
        API_URL,
        json={"query": event_search_query},
        headers=headers,
        timeout=30
    )
    data = response.json()

    if "data" in data and "__type" in data["data"] and data["data"]["__type"]:
        fields = data["data"]["__type"]["fields"]
        event_search = [f for f in fields if f["name"] == "eventSearch"]
        if event_search:
            args = event_search[0]["args"]
            print("Arguments:")
            for arg in args:
                type_name = arg["type"].get("name") or arg["type"].get("ofType", {}).get("name")
                print(f"  {arg['name']}: {type_name}")
        else:
            print("eventSearch not found")
    else:
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")

# Try a minimal working query
print("\n[3] Testing Minimal Query:")
print("-"*60)

minimal_query = """
query {
  eventSearch(filter: {query: "technology"}, first: 2) {
    edges {
      node {
        id
        title
      }
    }
  }
}
"""

try:
    response = requests.post(
        API_URL,
        json={"query": minimal_query},
        headers=headers,
        timeout=30
    )
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
