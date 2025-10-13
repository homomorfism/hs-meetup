import pytest
from datetime import date
from app.models import User, Group, Event


@pytest.mark.integration
class TestCompleteUserJourney:
    """Test complete user journey through the application."""

    def test_full_user_journey(self, client, db):
        """Test complete user flow: signup -> login -> create group -> create event -> attend."""
        # 1. Signup
        signup_response = client.post(
            "/api/auth/signup",
            json={
                "email": "journey@example.com",
                "password": "password123",
                "name": "Journey User",
                "location": "San Francisco"
            }
        )
        assert signup_response.status_code == 201
        user_id = signup_response.json()["id"]

        # 2. Login
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "journey@example.com",
                "password": "password123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Verify authenticated user
        me_response = client.get("/api/auth/me", headers=headers)
        assert me_response.status_code == 200

        # 4. Create a group
        group_response = client.post(
            "/api/groups/",
            json={
                "name": "My Tech Group",
                "description": "A group for tech enthusiasts",
                "category": "Technology",
                "location": "San Francisco, CA"
            },
            headers=headers
        )
        assert group_response.status_code == 201
        group_id = group_response.json()["id"]

        # 5. Create an event
        event_response = client.post(
            "/api/events/",
            json={
                "title": "My First Meetup",
                "description": "Let's meet up!",
                "date": "2025-12-20",
                "time": "18:00",
                "group_id": group_id,
                "location": "123 Main St",
                "location_city": "San Francisco",
                "category": "Technology",
                "price": "Free",
                "is_online": False,
                "max_attendees": 50
            },
            headers=headers
        )
        assert event_response.status_code == 201
        event_id = event_response.json()["id"]

        # 6. Verify user's groups
        user_groups_response = client.get(f"/api/users/{user_id}/groups")
        assert user_groups_response.status_code == 200
        assert len(user_groups_response.json()) == 1

        # 7. Verify user's events
        user_events_response = client.get(f"/api/users/{user_id}/events")
        assert user_events_response.status_code == 200
        assert len(user_events_response.json()) == 1

        # 8. Verify group's events
        group_events_response = client.get(f"/api/groups/{group_id}/events")
        assert group_events_response.status_code == 200
        assert len(group_events_response.json()) == 1


@pytest.mark.integration
class TestMultiUserInteractions:
    """Test interactions between multiple users."""

    def test_two_users_group_event_interaction(self, client, db):
        """Test two users interacting with group and event."""
        # User 1: Create account and group
        signup1 = client.post(
            "/api/auth/signup",
            json={
                "email": "user1@example.com",
                "password": "password123",
                "name": "User One"
            }
        )
        assert signup1.status_code == 201

        login1 = client.post(
            "/api/auth/login",
            data={"username": "user1@example.com", "password": "password123"}
        )
        token1 = login1.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}

        group_response = client.post(
            "/api/groups/",
            json={
                "name": "Shared Group",
                "category": "Technology",
                "location": "San Francisco"
            },
            headers=headers1
        )
        group_id = group_response.json()["id"]

        event_response = client.post(
            "/api/events/",
            json={
                "title": "Shared Event",
                "date": "2025-12-20",
                "time": "18:00",
                "group_id": group_id,
                "location_city": "San Francisco",
                "category": "Technology",
                "price": "Free",
                "is_online": False
            },
            headers=headers1
        )
        event_id = event_response.json()["id"]

        # User 2: Create account, join group, attend event
        signup2 = client.post(
            "/api/auth/signup",
            json={
                "email": "user2@example.com",
                "password": "password123",
                "name": "User Two"
            }
        )
        assert signup2.status_code == 201
        user2_id = signup2.json()["id"]

        login2 = client.post(
            "/api/auth/login",
            data={"username": "user2@example.com", "password": "password123"}
        )
        token2 = login2.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        # Join group
        join_response = client.post(
            f"/api/groups/{group_id}/join",
            headers=headers2
        )
        assert join_response.status_code == 200

        # Attend event
        attend_response = client.post(
            f"/api/events/{event_id}/attend",
            headers=headers2
        )
        assert attend_response.status_code == 200

        # Verify member in group
        members_response = client.get(f"/api/groups/{group_id}/members")
        members = members_response.json()
        assert any(member["id"] == user2_id for member in members)

        # Verify attendee in event
        attendees_response = client.get(f"/api/events/{event_id}/attendees")
        attendees = attendees_response.json()
        assert any(attendee["id"] == user2_id for attendee in attendees)


@pytest.mark.integration
class TestCascadingDeletes:
    """Test cascading deletes in the database."""

    def test_delete_user_removes_organized_content(self, client, db, test_user, test_group, test_event):
        """Test that deleting user removes their organized groups and events."""
        user_id = test_user.id
        group_id = test_group.id
        event_id = test_event.id

        # Delete user
        db.delete(test_user)
        db.commit()

        # Verify group is deleted (cascade)
        group = db.query(Group).filter(Group.id == group_id).first()
        assert group is None

        # Verify event is deleted (cascade)
        event = db.query(Event).filter(Event.id == event_id).first()
        assert event is None

    def test_delete_group_removes_events(self, client, db, test_group, test_event):
        """Test that deleting group removes its events."""
        group_id = test_group.id
        event_id = test_event.id

        # Delete group
        db.delete(test_group)
        db.commit()

        # Verify event is deleted (cascade)
        event = db.query(Event).filter(Event.id == event_id).first()
        assert event is None


@pytest.mark.integration
class TestCountUpdates:
    """Test that member and attendee counts are properly updated."""

    def test_group_member_count_updates(self, client, db, test_group, test_user2, auth_headers2):
        """Test that group member count increases when users join."""
        initial_count = test_group.members_count

        # User joins group
        response = client.post(
            f"/api/groups/{test_group.id}/join",
            headers=auth_headers2
        )
        assert response.status_code == 200

        # Verify count increased
        db.refresh(test_group)
        assert test_group.members_count == initial_count + 1

    def test_event_attendee_count_updates(self, client, db, test_event, test_user2, auth_headers2):
        """Test that event attendee count increases when users attend."""
        initial_count = test_event.attendees_count

        # User attends event
        response = client.post(
            f"/api/events/{test_event.id}/attend",
            headers=auth_headers2
        )
        assert response.status_code == 200

        # Verify count increased
        db.refresh(test_event)
        assert test_event.attendees_count == initial_count + 1


@pytest.mark.integration
class TestSearchAndDiscovery:
    """Test search and discovery features across the application."""

    def test_event_discovery_workflow(self, client, db, test_user, test_group):
        """Test event discovery through various filters."""
        # Create diverse events
        events = [
            Event(
                title="Python Workshop",
                description="Learn Python",
                date=date(2025, 12, 15),
                time="18:00",
                group_id=test_group.id,
                organizer_id=test_user.id,
                location_city="San Francisco",
                category="Technology",
                price="Free",
                is_online=True
            ),
            Event(
                title="JavaScript Meetup",
                description="JS discussion",
                date=date(2025, 12, 16),
                time="19:00",
                group_id=test_group.id,
                organizer_id=test_user.id,
                location_city="New York",
                category="Technology",
                price="$10",
                is_online=False
            ),
            Event(
                title="Yoga Session",
                description="Morning yoga",
                date=date(2025, 12, 17),
                time="08:00",
                group_id=test_group.id,
                organizer_id=test_user.id,
                location_city="San Francisco",
                category="Sports",
                price="Free",
                is_online=False
            ),
        ]
        for event in events:
            db.add(event)
        db.commit()

        # Search by keyword
        response = client.get("/api/events/?keyword=Python")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # Filter by location
        response = client.get("/api/events/?location=San Francisco")
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Filter by category
        response = client.get("/api/events/?category=Technology")
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Filter by online status
        response = client.get("/api/events/?is_online=true")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # Filter by price
        response = client.get("/api/events/?price=free")
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Multiple filters
        response = client.get(
            "/api/events/?location=San Francisco&category=Technology&is_online=true"
        )
        assert response.status_code == 200
        assert len(response.json()) == 1


@pytest.mark.integration
class TestAuthenticationFlow:
    """Test authentication across different endpoints."""

    def test_protected_endpoints_require_auth(self, client):
        """Test that protected endpoints reject unauthenticated requests."""
        # Try to create group without auth
        response = client.post(
            "/api/groups/",
            json={"name": "Test", "category": "Technology"}
        )
        assert response.status_code == 401

        # Try to update user without auth
        response = client.put(
            "/api/users/1",
            json={"name": "Hacker"}
        )
        assert response.status_code == 401

        # Try to create event without auth
        response = client.post(
            "/api/events/",
            json={
                "title": "Test",
                "date": "2025-12-20",
                "time": "18:00",
                "group_id": 1,
                "location_city": "SF",
                "category": "Technology",
                "price": "Free",
                "is_online": False
            }
        )
        assert response.status_code == 401

    def test_public_endpoints_accessible(self, client, test_user, test_group, test_event):
        """Test that public endpoints are accessible without auth."""
        # List users
        response = client.get("/api/users/")
        assert response.status_code == 200

        # Get user
        response = client.get(f"/api/users/{test_user.id}")
        assert response.status_code == 200

        # List groups
        response = client.get("/api/groups/")
        assert response.status_code == 200

        # Get group
        response = client.get(f"/api/groups/{test_group.id}")
        assert response.status_code == 200

        # List events
        response = client.get("/api/events/")
        assert response.status_code == 200

        # Get event
        response = client.get(f"/api/events/{test_event.id}")
        assert response.status_code == 200
