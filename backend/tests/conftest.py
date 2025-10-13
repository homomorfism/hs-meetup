import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app
from app.models import User, Group, Event, Category
from app.core.security import get_password_hash, create_access_token
from datetime import timedelta, date
from faker import Faker

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

fake = Faker()


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with the test database."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User(
        email="testuser@example.com",
        password_hash=get_password_hash("password123"),
        name="Test User",
        location="San Francisco",
        bio="Test bio",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user2(db):
    """Create a second test user."""
    user = User(
        email="testuser2@example.com",
        password_hash=get_password_hash("password123"),
        name="Test User 2",
        location="New York",
        bio="Test bio 2",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user):
    """Create an authentication token for test_user."""
    access_token = create_access_token(
        data={"sub": test_user.email},
        expires_delta=timedelta(minutes=30)
    )
    return access_token


@pytest.fixture
def auth_token2(test_user2):
    """Create an authentication token for test_user2."""
    access_token = create_access_token(
        data={"sub": test_user2.email},
        expires_delta=timedelta(minutes=30)
    )
    return access_token


@pytest.fixture
def auth_headers(auth_token):
    """Create authentication headers."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def auth_headers2(auth_token2):
    """Create authentication headers for user 2."""
    return {"Authorization": f"Bearer {auth_token2}"}


@pytest.fixture
def test_category(db):
    """Create a test category."""
    category = Category(
        name="Technology",
        icon="💻",
        color="#3B82F6",
        slug="technology"
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@pytest.fixture
def test_group(db, test_user, test_category):
    """Create a test group."""
    group = Group(
        name="Tech Enthusiasts",
        description="A group for tech lovers",
        category="Technology",
        location="San Francisco, CA",
        organizer_id=test_user.id,
        members_count=1
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


@pytest.fixture
def test_event(db, test_user, test_group):
    """Create a test event."""
    event = Event(
        title="Tech Meetup",
        description="Monthly tech meetup",
        date=date(2025, 12, 15),
        time="18:00",
        duration="2 hours",
        group_id=test_group.id,
        organizer_id=test_user.id,
        location="123 Main St",
        location_city="San Francisco",
        attendees_count=0,
        max_attendees=50,
        price="Free",
        is_online=False,
        category="Technology"
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@pytest.fixture
def multiple_users(db):
    """Create multiple test users."""
    users = []
    for i in range(5):
        user = User(
            email=f"user{i}@example.com",
            password_hash=get_password_hash("password123"),
            name=fake.name(),
            location=fake.city(),
            bio=fake.text(max_nb_chars=100),
            is_active=True
        )
        db.add(user)
        users.append(user)
    db.commit()
    for user in users:
        db.refresh(user)
    return users


@pytest.fixture
def multiple_groups(db, test_user):
    """Create multiple test groups."""
    groups = []
    categories = ["Technology", "Sports", "Arts", "Business"]
    for i, cat in enumerate(categories):
        group = Group(
            name=f"Group {i+1}",
            description=f"Description for group {i+1}",
            category=cat,
            location=fake.city(),
            organizer_id=test_user.id,
            members_count=0
        )
        db.add(group)
        groups.append(group)
    db.commit()
    for group in groups:
        db.refresh(group)
    return groups


@pytest.fixture
def multiple_events(db, test_user, test_group):
    """Create multiple test events."""
    events = []
    for i in range(5):
        event = Event(
            title=f"Event {i+1}",
            description=f"Description for event {i+1}",
            date=date(2025, 12, 15 + i),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location=fake.address(),
            location_city=fake.city(),
            attendees_count=0,
            price="Free" if i % 2 == 0 else "$10",
            is_online=i % 2 == 0,
            category="Technology"
        )
        db.add(event)
        events.append(event)
    db.commit()
    for event in events:
        db.refresh(event)
    return events
