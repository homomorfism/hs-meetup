import pytest
from datetime import date
from app.models import Event, Group
from fastapi.testclient import TestClient

class TestListEvents:
    """Test list events endpoint."""

    def test_list_events_success(self, client, multiple_events):
        """Test listing all events."""
        response = client.get("/api/events/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert all("title" in event for event in data)

    def test_list_events_empty(self, client):
        """Test listing events when database is empty."""
        response = client.get("/api/events/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_events_pagination(self, client: TestClient, multiple_events):
        """Test event list pagination."""
        response = client.get("/api/events/?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        response = client.get("/api/events/?skip=2&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_list_events_filter_by_keyword(self, client, db, test_user, test_group):
        """Test filtering events by keyword in title/description."""
        event1 = Event(
            title="Python Workshop",
            description="Learn Python programming",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        event2 = Event(
            title="JavaScript Meetup",
            description="Discuss JavaScript trends",
            date=date(2025, 12, 16),
            time="19:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        db.add_all([event1, event2])
        db.commit()

        response = client.get("/api/events/?keyword=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Python" in data[0]["title"]

    def test_list_events_filter_by_location(self, client, db, test_user, test_group):
        """Test filtering events by location."""
        event1 = Event(
            title="SF Event",
            description="In San Francisco",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        event2 = Event(
            title="NY Event",
            description="In New York",
            date=date(2025, 12, 16),
            time="19:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="New York",
            category="Technology",
            price="Free",
            is_online=False
        )
        db.add_all([event1, event2])
        db.commit()

        response = client.get("/api/events/?location=San Francisco")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "San Francisco" in data[0]["location_city"]

    def test_list_events_filter_by_category(self, client, db, test_user, test_group):
        """Test filtering events by category."""
        event1 = Event(
            title="Tech Event",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        event2 = Event(
            title="Sports Event",
            date=date(2025, 12, 16),
            time="19:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Sports",
            price="Free",
            is_online=False
        )
        db.add_all([event1, event2])
        db.commit()

        response = client.get("/api/events/?category=Technology")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "Technology"

    def test_list_events_filter_by_is_online(self, client, multiple_events):
        """Test filtering events by online/offline status."""
        response = client.get("/api/events/?is_online=true")
        assert response.status_code == 200
        data = response.json()
        assert all(event["is_online"] for event in data)

        response = client.get("/api/events/?is_online=false")
        assert response.status_code == 200
        data = response.json()
        assert all(not event["is_online"] for event in data)

    def test_list_events_filter_by_price_free(self, client, multiple_events):
        """Test filtering events by free price."""
        response = client.get("/api/events/?price=free")
        assert response.status_code == 200
        data = response.json()
        assert all("free" in event["price"].lower() for event in data)

    def test_list_events_filter_by_price_paid(self, client, multiple_events):
        """Test filtering events by paid price."""
        response = client.get("/api/events/?price=paid")
        assert response.status_code == 200
        data = response.json()
        assert all("free" not in event["price"].lower() for event in data)

    def test_list_events_multiple_filters(self, client, db, test_user, test_group):
        """Test filtering events by multiple criteria."""
        event = Event(
            title="Online Python Workshop",
            description="Free online Python workshop",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=True
        )
        db.add(event)
        db.commit()

        response = client.get(
            "/api/events/?category=Technology&is_online=true&price=free"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1


class TestGetEvent:
    """Test get event endpoint."""

    def test_get_event_success(self, client, test_event):
        """Test getting a specific event."""
        response = client.get(f"/api/events/{test_event.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_event.id
        assert data["title"] == test_event.title
        assert data["group_id"] == test_event.group_id

    def test_get_event_not_found(self, client):
        """Test getting non-existent event."""
        response = client.get("/api/events/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_event_invalid_id(self, client):
        """Test getting event with invalid ID."""
        response = client.get("/api/events/invalid")
        assert response.status_code == 422


class TestCreateEvent:
    """Test create event endpoint."""

    def test_create_event_success(self, client, test_group, auth_headers):
        """Test creating a new event."""
        response = client.post(
            "/api/events/",
            json={
                "title": "New Event",
                "description": "A new test event",
                "date": "2025-12-20",
                "time": "18:00",
                "duration": "2 hours",
                "group_id": test_group.id,
                "location": "123 Main St",
                "location_city": "San Francisco",
                "category": "Technology",
                "price": "Free",
                "is_online": False,
                "max_attendees": 100
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Event"
        assert data["group_id"] == test_group.id
        assert "id" in data

    def test_create_event_unauthorized(self, client, test_group):
        """Test creating event without authentication."""
        response = client.post(
            "/api/events/",
            json={
                "title": "Unauthorized Event",
                "date": "2025-12-20",
                "time": "18:00",
                "group_id": test_group.id,
                "location_city": "San Francisco",
                "category": "Technology",
                "price": "Free",
                "is_online": False
            }
        )
        assert response.status_code == 401

    def test_create_event_group_not_found(self, client, auth_headers):
        """Test creating event for non-existent group."""
        response = client.post(
            "/api/events/",
            json={
                "title": "Event",
                "date": "2025-12-20",
                "time": "18:00",
                "group_id": 9999,
                "location_city": "San Francisco",
                "category": "Technology",
                "price": "Free",
                "is_online": False
            },
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_create_event_not_organizer(self, client, test_group, auth_headers2):
        """Test creating event by non-organizer."""
        response = client.post(
            "/api/events/",
            json={
                "title": "Unauthorized Event",
                "date": "2025-12-20",
                "time": "18:00",
                "group_id": test_group.id,
                "location_city": "San Francisco",
                "category": "Technology",
                "price": "Free",
                "is_online": False
            },
            headers=auth_headers2
        )
        assert response.status_code == 403
        assert "organizer" in response.json()["detail"].lower()

    def test_create_event_missing_required_fields(self, client, test_group, auth_headers):
        """Test creating event with missing required fields."""
        response = client.post(
            "/api/events/",
            json={"title": "Incomplete Event"},
            headers=auth_headers
        )
        assert response.status_code == 422


class TestUpdateEvent:
    """Test update event endpoint."""

    def test_update_event_success(self, client, test_event, auth_headers):
        """Test updating an event."""
        response = client.put(
            f"/api/events/{test_event.id}",
            json={
                "title": "Updated Event Title",
                "description": "Updated description"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Event Title"
        assert data["description"] == "Updated description"

    def test_update_event_unauthorized(self, client, test_event):
        """Test updating event without authentication."""
        response = client.put(
            f"/api/events/{test_event.id}",
            json={"title": "Hacker Event"}
        )
        assert response.status_code == 401

    def test_update_event_forbidden(self, client, test_event, auth_headers2):
        """Test updating event by non-organizer."""
        response = client.put(
            f"/api/events/{test_event.id}",
            json={"title": "Unauthorized Update"},
            headers=auth_headers2
        )
        assert response.status_code == 403
        assert "not authorized" in response.json()["detail"].lower()

    def test_update_event_not_found(self, client, auth_headers):
        """Test updating non-existent event."""
        response = client.put(
            "/api/events/9999",
            json={"title": "Ghost Event"},
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_update_event_partial(self, client, test_event, auth_headers):
        """Test partial update of event."""
        original_category = test_event.category
        response = client.put(
            f"/api/events/{test_event.id}",
            json={"title": "New Title Only"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title Only"
        assert data["category"] == original_category


class TestAttendEvent:
    """Test attend event endpoint."""

    def test_attend_event_success(self, client, test_event, auth_headers2, db):
        """Test attending an event."""
        initial_count = test_event.attendees_count
        response = client.post(
            f"/api/events/{test_event.id}/attend",
            headers=auth_headers2
        )
        assert response.status_code == 200
        assert "success" in response.json()["message"].lower()

        # Verify attendee count increased
        db.refresh(test_event)
        assert test_event.attendees_count == initial_count + 1

    def test_attend_event_idempotent(self, client, test_event, auth_headers2, db):
        """Test attending same event twice is idempotent."""
        # Attend first time
        response1 = client.post(
            f"/api/events/{test_event.id}/attend",
            headers=auth_headers2
        )
        assert response1.status_code == 200
        db.refresh(test_event)
        count_after_first = test_event.attendees_count

        # Attend second time
        response2 = client.post(
            f"/api/events/{test_event.id}/attend",
            headers=auth_headers2
        )
        assert response2.status_code == 200
        db.refresh(test_event)
        assert test_event.attendees_count == count_after_first

    def test_attend_event_at_capacity(self, client, db, test_user, test_group, auth_headers2):
        """Test attending event that is at max capacity."""
        # Create event with max_attendees=1
        event = Event(
            title="Full Event",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False,
            max_attendees=1,
            attendees_count=1
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        response = client.post(
            f"/api/events/{event.id}/attend",
            headers=auth_headers2
        )
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()

    def test_attend_event_unauthorized(self, client, test_event):
        """Test attending event without authentication."""
        response = client.post(f"/api/events/{test_event.id}/attend")
        assert response.status_code == 401

    def test_attend_event_not_found(self, client, auth_headers):
        """Test attending non-existent event."""
        response = client.post("/api/events/9999/attend", headers=auth_headers)
        assert response.status_code == 404


class TestGetEventAttendees:
    """Test get event attendees endpoint."""

    def test_get_event_attendees_success(self, client, db, test_event, test_user2):
        """Test getting attendees of an event."""
        # Add attendee to event
        test_event.attendees.append(test_user2)
        db.commit()

        response = client.get(f"/api/events/{test_event.id}/attendees")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(attendee["id"] == test_user2.id for attendee in data)

    def test_get_event_attendees_empty(self, client, test_event):
        """Test getting attendees for event with no attendees."""
        response = client.get(f"/api/events/{test_event.id}/attendees")
        assert response.status_code == 200
        # Could be empty list

    def test_get_event_attendees_not_found(self, client):
        """Test getting attendees for non-existent event."""
        response = client.get("/api/events/9999/attendees")
        assert response.status_code == 404

    def test_get_event_attendees_pagination(self, client, db, test_event, multiple_users):
        """Test event attendees pagination."""
        # Add multiple attendees
        for user in multiple_users[:4]:
            test_event.attendees.append(user)
        db.commit()

        response = client.get(f"/api/events/{test_event.id}/attendees?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2
