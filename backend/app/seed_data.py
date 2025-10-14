import json
from datetime import datetime
from pathlib import Path
import traceback
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import SessionLocal, engine
from .models import User, Category, Group, Event, user_interests
from .core.security import get_password_hash
from pyrootutils import find_root
from .database import Base

INITIAL_DATA_DIR = Path("__file__").parent / "initial_data"

def load_json_file(filename: str) -> list:
    """Load JSON data from initial_data directory"""
    filepath = INITIAL_DATA_DIR / filename
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filename} not found in {INITIAL_DATA_DIR}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing {filename}: {e}")
        return []

def seed_database():
    # Drop all tables and recreate them to ensure schema is up to date
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating tables with new schema...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        print("Seeding database...")

        # Seed categories
        categories_data = load_json_file("categories.json")
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)

        db.commit()
        print(f"✓ Seeded {len(categories_data)} categories")

        users_data = load_json_file("users.json")

        # Create a mapping of category names to category objects
        categories_by_name = {cat.name: cat for cat in db.query(Category).all()}

        # Store friends data for later processing (after all users are created)
        user_friends_map = {}

        for user_data in users_data:
            # Extract interests (category names)
            interests = user_data.pop("interests", [])

            # Extract friends (user IDs) - we'll add them after all users are created
            friends_ids = user_data.pop("friends", [])
            user_id = user_data.get("id")
            if friends_ids:
                user_friends_map[user_id] = friends_ids

            # Remove password field and use hashed password
            password = user_data.pop("password")
            # Parse member_since date
            member_since = datetime.fromisoformat(user_data.pop("member_since"))

            user = User(
                **user_data,
                password_hash=get_password_hash(password),
                member_since=member_since
            )

            # Add user interests
            for interest_name in interests:
                if interest_name in categories_by_name:
                    user.interests.append(categories_by_name[interest_name])

            db.add(user)

        db.commit()
        print(f"✓ Seeded {len(users_data)} users (password: password123)")

        # Now add friendships (bidirectional)
        print("Adding friendships...")
        added_friendships = set()  # Track friendships to avoid duplicates

        for user_id, friend_ids in user_friends_map.items():
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                continue

            for friend_id in friend_ids:
                # Create a sorted tuple to represent the friendship (to avoid duplicates)
                friendship_key = tuple(sorted([user_id, friend_id]))

                if friendship_key in added_friendships:
                    continue  # Skip if already added

                friend = db.query(User).filter(User.id == friend_id).first()
                if friend and friend not in user.friends:
                    # Add bidirectional friendship
                    user.friends.append(friend)
                    friend.friends.append(user)
                    added_friendships.add(friendship_key)

        db.commit()
        print(f"✓ Added {len(added_friendships)} friendships")

        # Seed groups
        groups_data = load_json_file("groups.json")
        for group_data in groups_data:
            # Parse founded date
            founded = datetime.fromisoformat(group_data.pop("founded"))
            # Rename 'organizer' to 'organizer_id'
            if "organizer" in group_data:
                group_data["organizer_id"] = group_data.pop("organizer")

            group = Group(
                **group_data,
                founded=founded
            )
            db.add(group)

        db.commit()
        print(f"✓ Seeded {len(groups_data)} groups")

        # Seed events
        events_data = load_json_file("events.json")
        for event_data in events_data:
            # Parse date
            event_date = datetime.fromisoformat(event_data.pop("date"))

            # Extract attendees list (user IDs)
            attendees_ids = event_data.pop("attendees", [])

            # Rename fields to match model
            if "isOnline" in event_data:
                event_data["is_online"] = event_data.pop("isOnline")
            if "locationCity" in event_data:
                event_data["location_city"] = event_data.pop("locationCity")

            # Create event
            event = Event(
                **event_data,
                date=event_date
            )

            # Add attendees relationships
            if attendees_ids:
                attendee_users = db.query(User).filter(User.id.in_(attendees_ids)).all()
                event.attendees.extend(attendee_users)

            db.add(event)

        db.commit()
        print(f"✓ Seeded {len(events_data)} events")

        # Reset sequences to prevent duplicate key errors
        print("\nResetting ID sequences...")
        try:
            db.execute(text("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));"))
            db.execute(text("SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));"))
            db.execute(text("SELECT setval('groups_id_seq', (SELECT MAX(id) FROM groups));"))
            db.execute(text("SELECT setval('events_id_seq', (SELECT MAX(id) FROM events));"))
            db.commit()
            print("✓ Sequences reset successfully")
        except Exception as seq_error:
            print(f"Warning: Could not reset sequences: {seq_error}")

        print("\n✅ Database seeded successfully!")
        print("\nSample User Credentials (all users have same password):")
        print("Email: sarah.johnson@example.com | Password: password123")
        print("Email: michael.chen@example.com | Password: password123")
        print("Email: emily.rodriguez@example.com | Password: password123")
        print("...and more (check users.json for all users)")

    except Exception as e:
        print(f"Error seeding database: {e}")
        print(traceback.format_exc())
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
