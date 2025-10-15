"""
Quick script to add Barcelona events for testing
"""
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Event, Group, User

def add_barcelona_events():
    db = SessionLocal()

    try:
        # Get first user as organizer
        user = db.query(User).first()
        if not user:
            print("Error: No users found")
            return

        # Get or create a Barcelona group
        group = db.query(Group).filter(Group.name == "Barcelona Tech Meetup").first()
        if not group:
            group = Group(
                name="Barcelona Tech Meetup",
                description="Technology events in Barcelona",
                category="Technology",
                location="Barcelona, Spain",
                members_count=250,
                organizer_id=user.id,
                founded=datetime(2020, 1, 1)
            )
            db.add(group)
            db.flush()
            print(f"✓ Created group: {group.name}")

        # Barcelona events data
        barcelona_events = [
            {
                "title": "Barcelona Tech Talks: AI & Machine Learning",
                "description": "Join us for an evening of AI and ML discussions in the heart of Barcelona.",
                "location": "Carrer de Pelai, 12",
                "location_city": "Barcelona, Spain",
                "latitude": 41.3851,
                "longitude": 2.1734,
                "category": "Technology",
                "days_ahead": 3,
                "time": "19:00"
            },
            {
                "title": "Barcelona Startup Networking Night",
                "description": "Connect with fellow entrepreneurs and startup enthusiasts in Barcelona.",
                "location": "Plaça de Catalunya, 1",
                "location_city": "Barcelona, Spain",
                "latitude": 41.3870,
                "longitude": 2.1700,
                "category": "Business & Professional",
                "days_ahead": 5,
                "time": "18:30"
            },
            {
                "title": "Coding Workshop: Python for Beginners",
                "description": "Learn Python programming basics in this hands-on workshop at Barcelona Tech Hub.",
                "location": "Carrer de Mallorca, 208",
                "location_city": "Barcelona, Spain",
                "latitude": 41.3950,
                "longitude": 2.1620,
                "category": "Learning & Education",
                "days_ahead": 7,
                "time": "17:00"
            },
            {
                "title": "Barcelona Beach Cleanup & Social",
                "description": "Help clean Barceloneta Beach while meeting new people!",
                "location": "Platja de la Barceloneta",
                "location_city": "Barcelona, Spain",
                "latitude": 41.3771,
                "longitude": 2.1905,
                "category": "Outdoors & Adventure",
                "days_ahead": 2,
                "time": "10:00"
            },
            {
                "title": "Web Development Bootcamp - React & Node.js",
                "description": "Intensive weekend bootcamp covering modern web development technologies.",
                "location": "Carrer del Consell de Cent, 425",
                "location_city": "Barcelona, Spain",
                "latitude": 41.3930,
                "longitude": 2.1655,
                "category": "Technology",
                "days_ahead": 10,
                "time": "09:00"
            },
            {
                "title": "Barcelona Language Exchange",
                "description": "Practice Spanish, Catalan, English, or other languages with locals and expats.",
                "location": "Carrer de Ferran, 28",
                "location_city": "Barcelona, Spain",
                "latitude": 41.3822,
                "longitude": 2.1750,
                "category": "Learning & Education",
                "days_ahead": 1,
                "time": "20:00"
            },
            {
                "title": "Photography Walk: Gothic Quarter",
                "description": "Explore and photograph Barcelona's historic Gothic Quarter with fellow photographers.",
                "location": "Plaça de Sant Jaume",
                "location_city": "Barcelona, Spain",
                "latitude": 41.3825,
                "longitude": 2.1768,
                "category": "Arts & Culture",
                "days_ahead": 4,
                "time": "16:00"
            },
            {
                "title": "Barcelona Blockchain Summit",
                "description": "Annual blockchain and cryptocurrency conference featuring industry leaders.",
                "location": "Fira de Barcelona",
                "location_city": "Barcelona, Spain",
                "latitude": 41.3527,
                "longitude": 2.1248,
                "category": "Technology",
                "days_ahead": 14,
                "time": "09:00"
            }
        ]

        added_count = 0
        for event_data in barcelona_events:
            # Check if event already exists
            existing = db.query(Event).filter(Event.title == event_data["title"]).first()
            if existing:
                print(f"⊘ Skipped: {event_data['title']} (already exists)")
                continue

            # Calculate future date
            event_date = datetime.now() + timedelta(days=event_data["days_ahead"])

            event = Event(
                title=event_data["title"],
                description=event_data["description"],
                date=event_date.date(),
                time=event_data["time"],
                location=event_data["location"],
                location_city=event_data["location_city"],
                latitude=event_data["latitude"],
                longitude=event_data["longitude"],
                is_online=False,
                category=event_data["category"],
                image=f"https://source.unsplash.com/800x600/?barcelona,{event_data['category'].lower()}",
                price="Free",
                max_attendees=50,
                group_id=group.id,
                organizer_id=user.id
            )
            db.add(event)
            added_count += 1
            print(f"✓ Added: {event.title}")

        db.commit()
        print(f"\n✅ Successfully added {added_count} Barcelona events!")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Adding Barcelona Events to Database")
    print("=" * 60)
    add_barcelona_events()
