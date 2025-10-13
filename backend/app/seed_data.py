import sys
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, User, Category, Group, Event, user_interests
from app.core.security import get_password_hash

# Import frontend data
sys.path.append('../frontend/src')

def seed_database():
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).count() > 0:
            print("Database already seeded!")
            return

        print("Seeding database...")

        # Seed categories
        categories_data = [
            {"id": 1, "name": "Technology", "icon": "💻", "slug": "technology"},
            {"id": 2, "name": "Arts & Culture", "icon": "🎨", "slug": "arts-culture"},
            {"id": 3, "name": "Sports & Fitness", "icon": "⚽", "slug": "sports-fitness"},
            {"id": 4, "name": "Food & Drink", "icon": "🍕", "slug": "food-drink"},
            {"id": 5, "name": "Social Activities", "icon": "🎉", "slug": "social-activities"},
            {"id": 6, "name": "Travel & Outdoor", "icon": "🏔️", "slug": "travel-outdoor"},
            {"id": 7, "name": "Music", "icon": "🎵", "slug": "music"},
            {"id": 8, "name": "Books & Writing", "icon": "📚", "slug": "books-writing"},
            {"id": 9, "name": "Film & Photography", "icon": "📷", "slug": "film-photography"},
            {"id": 10, "name": "Games", "icon": "🎮", "slug": "games"},
            {"id": 11, "name": "Health & Wellness", "icon": "🧘", "slug": "health-wellness"},
            {"id": 12, "name": "Business & Career", "icon": "💼", "slug": "business-career"},
        ]

        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)

        db.commit()
        print(f"✓ Seeded {len(categories_data)} categories")

        # Seed users (with password: password123)
        default_password = get_password_hash("password123")

        # Add test users
        test_users = [
            {"id": 1, "email": "test1@example.com", "name": "Test User 1", "location": "San Francisco, CA"},
            {"id": 2, "email": "test2@example.com", "name": "Test User 2", "location": "New York, NY"},
            {"id": 3, "email": "test3@example.com", "name": "Test User 3", "location": "Los Angeles, CA"},
            {"id": 4, "email": "test4@example.com", "name": "Test User 4", "location": "Chicago, IL"},
            {"id": 5, "email": "test5@example.com", "name": "Test User 5", "location": "Seattle, WA"},
        ]

        for user_data in test_users:
            user = User(
                **user_data,
                password_hash=default_password,
                bio=f"Test user account for {user_data['name']}",
                avatar=f"https://i.pravatar.cc/150?u={user_data['id']}",
                member_since=datetime(2024, 1, 1)
            )
            db.add(user)

        # Seed remaining users from frontend (id 6-20)
        users_data = [
            {"id": 6, "name": "James Wilson", "email": "james.wilson@example.com", "bio": "Board game enthusiast and event organizer.", "location": "Chicago, IL", "avatar": "https://i.pravatar.cc/150?img=14", "member_since": "2019-04-18"},
            {"id": 7, "name": "Lisa Anderson", "email": "lisa.anderson@example.com", "bio": "Book lover and aspiring author. Let's discuss great literature!", "location": "Boston, MA", "avatar": "https://i.pravatar.cc/150?img=10", "member_since": "2021-05-30"},
            {"id": 8, "name": "Robert Taylor", "email": "robert.taylor@example.com", "bio": "Photographer and travel blogger exploring the world one city at a time.", "location": "Portland, OR", "avatar": "https://i.pravatar.cc/150?img=15", "member_since": "2020-02-14"},
            {"id": 9, "name": "Amanda White", "email": "amanda.white@example.com", "bio": "Music producer and DJ. Electronic beats are my life.", "location": "Miami, FL", "avatar": "https://i.pravatar.cc/150?img=20", "member_since": "2019-09-08"},
            {"id": 10, "name": "Chris Brown", "email": "chris.brown@example.com", "bio": "Entrepreneur and startup mentor. Happy to share my experience!", "location": "San Francisco, CA", "avatar": "https://i.pravatar.cc/150?img=33", "member_since": "2018-07-12"},
            {"id": 11, "name": "Maria Garcia", "email": "maria.garcia@example.com", "bio": "Yoga teacher and meditation guide finding peace in chaos.", "location": "San Diego, CA", "avatar": "https://i.pravatar.cc/150?img=23", "member_since": "2021-03-25"},
            {"id": 12, "name": "Kevin Lee", "email": "kevin.lee@example.com", "bio": "Gaming streamer and esports enthusiast.", "location": "Denver, CO", "avatar": "https://i.pravatar.cc/150?img=51", "member_since": "2020-10-15"},
            {"id": 13, "name": "Sophie Turner", "email": "sophie.turner@example.com", "bio": "Wine enthusiast and sommelier in training.", "location": "Napa, CA", "avatar": "https://i.pravatar.cc/150?img=24", "member_since": "2019-12-01"},
            {"id": 14, "name": "Daniel Murphy", "email": "daniel.murphy@example.com", "bio": "Rock climbing instructor and outdoor adventure guide.", "location": "Boulder, CO", "avatar": "https://i.pravatar.cc/150?img=52", "member_since": "2020-06-08"},
            {"id": 15, "name": "Rachel Green", "email": "rachel.green@example.com", "bio": "Fashion designer and art gallery curator.", "location": "New York, NY", "avatar": "https://i.pravatar.cc/150?img=27", "member_since": "2021-07-19"},
            {"id": 16, "name": "Tom Harris", "email": "tom.harris@example.com", "bio": "Film critic and indie movie lover.", "location": "Los Angeles, CA", "avatar": "https://i.pravatar.cc/150?img=53", "member_since": "2019-02-28"},
            {"id": 17, "name": "Nicole Davis", "email": "nicole.davis@example.com", "bio": "Marathon organizer and running coach.", "location": "Chicago, IL", "avatar": "https://i.pravatar.cc/150?img=29", "member_since": "2020-04-11"},
            {"id": 18, "name": "Alex Thompson", "email": "alex.thompson@example.com", "bio": "Jazz musician and music theory teacher.", "location": "New Orleans, LA", "avatar": "https://i.pravatar.cc/150?img=54", "member_since": "2018-09-22"},
            {"id": 19, "name": "Laura Mitchell", "email": "laura.mitchell@example.com", "bio": "Food blogger and cooking class instructor.", "location": "Portland, OR", "avatar": "https://i.pravatar.cc/150?img=32", "member_since": "2021-08-05"},
            {"id": 20, "name": "Ryan Cooper", "email": "ryan.cooper@example.com", "bio": "AI researcher and tech conference speaker.", "location": "Seattle, WA", "avatar": "https://i.pravatar.cc/150?img=56", "member_since": "2019-11-17"},
        ]

        for user_data in users_data:
            member_since = datetime.fromisoformat(user_data.pop("member_since"))
            user = User(
                **user_data,
                password_hash=default_password,
                member_since=member_since
            )
            db.add(user)

        db.commit()
        print(f"✓ Seeded {len(test_users) + len(users_data)} users (password: password123)")

        print("\n✅ Database seeded successfully!")
        print("\nTest User Credentials:")
        print("Email: test1@example.com | Password: password123")
        print("Email: test2@example.com | Password: password123")
        print("Email: test3@example.com | Password: password123")
        print("Email: test4@example.com | Password: password123")
        print("Email: test5@example.com | Password: password123")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
