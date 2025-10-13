import pytest
from app.models import User, Group, Event
from datetime import date


class TestListUsers:
    """Test list users endpoint."""

    def test_list_users_success(self, client, multiple_users):
        """Test listing users."""
        response = client.get("/api/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert all("email" in user for user in data)
        assert all("name" in user for user in data)

    def test_list_users_empty(self, client):
        """Test listing users when database is empty."""
        response = client.get("/api/users/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_users_pagination(self, client, multiple_users):
        """Test user list pagination."""
        response = client.get("/api/users/?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        response = client.get("/api/users/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_users_skip_all(self, client, multiple_users):
        """Test skipping all users."""
        response = client.get("/api/users/?skip=10&limit=10")
        assert response.status_code == 200
        assert response.json() == []


class TestGetUser:
    """Test get user endpoint."""

    def test_get_user_success(self, client, test_user):
        """Test getting a specific user."""
        response = client.get(f"/api/users/{test_user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email
        assert data["name"] == test_user.name
        assert data["location"] == test_user.location
        assert "password_hash" not in data

    def test_get_user_not_found(self, client):
        """Test getting non-existent user."""
        response = client.get("/api/users/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_user_invalid_id(self, client):
        """Test getting user with invalid ID."""
        response = client.get("/api/users/invalid")
        assert response.status_code == 422


class TestUpdateUser:
    """Test update user endpoint."""

    def test_update_user_success(self, client, test_user, auth_headers):
        """Test updating user profile."""
        response = client.put(
            f"/api/users/{test_user.id}",
            json={
                "name": "Updated Name",
                "location": "New York",
                "bio": "Updated bio"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["location"] == "New York"
        assert data["bio"] == "Updated bio"

    def test_update_user_partial(self, client, test_user, auth_headers):
        """Test partial update of user profile."""
        response = client.put(
            f"/api/users/{test_user.id}",
            json={"name": "New Name Only"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name Only"
        assert data["location"] == test_user.location  # Unchanged

    def test_update_user_unauthorized(self, client, test_user):
        """Test updating user without authentication."""
        response = client.put(
            f"/api/users/{test_user.id}",
            json={"name": "Hacker Name"}
        )
        assert response.status_code == 401

    def test_update_user_forbidden(self, client, test_user, test_user2, auth_headers2):
        """Test updating another user's profile."""
        response = client.put(
            f"/api/users/{test_user.id}",
            json={"name": "Hacker Name"},
            headers=auth_headers2
        )
        assert response.status_code == 403
        assert "not authorized" in response.json()["detail"].lower()

    def test_update_user_not_found(self, client, auth_headers):
        """Test updating non-existent user."""
        response = client.put(
            "/api/users/9999",
            json={"name": "Ghost User"},
            headers=auth_headers
        )
        assert response.status_code == 403  # Will fail auth check first

    def test_update_user_empty_data(self, client, test_user, auth_headers):
        """Test updating user with empty data."""
        response = client.put(
            f"/api/users/{test_user.id}",
            json={},
            headers=auth_headers
        )
        assert response.status_code == 200
        # No changes should be made


class TestGetUserEvents:
    """Test get user events endpoint."""

    def test_get_user_events_success(self, client, db, test_user, test_group):
        """Test getting user's organized events."""
        # Create events for the user
        event1 = Event(
            title="Event 1",
            description="Description",
            date=date(2025, 12, 15),
            time="18:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location="Location 1",
            location_city="San Francisco",
            category="Technology",
            price="Free",
            is_online=False
        )
        event2 = Event(
            title="Event 2",
            description="Description",
            date=date(2025, 12, 16),
            time="19:00",
            group_id=test_group.id,
            organizer_id=test_user.id,
            location="Location 2",
            location_city="San Francisco",
            category="Technology",
            price="$10",
            is_online=True
        )
        db.add_all([event1, event2])
        db.commit()

        response = client.get(f"/api/users/{test_user.id}/events")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("title" in event for event in data)

    def test_get_user_events_empty(self, client, test_user):
        """Test getting events for user with no events."""
        response = client.get(f"/api/users/{test_user.id}/events")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_user_events_nonexistent_user(self, client):
        """Test getting events for non-existent user."""
        response = client.get("/api/users/9999/events")
        assert response.status_code == 200
        assert response.json() == []


class TestGetUserGroups:
    """Test get user groups endpoint."""

    def test_get_user_groups_success(self, client, db, test_user):
        """Test getting user's organized groups."""
        # Create groups for the user
        group1 = Group(
            name="Group 1",
            description="Description",
            category="Technology",
            location="San Francisco",
            organizer_id=test_user.id
        )
        group2 = Group(
            name="Group 2",
            description="Description",
            category="Sports",
            location="New York",
            organizer_id=test_user.id
        )
        db.add_all([group1, group2])
        db.commit()

        response = client.get(f"/api/users/{test_user.id}/groups")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("name" in group for group in data)

    def test_get_user_groups_empty(self, client, test_user):
        """Test getting groups for user with no groups."""
        response = client.get(f"/api/users/{test_user.id}/groups")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_user_groups_nonexistent_user(self, client):
        """Test getting groups for non-existent user."""
        response = client.get("/api/users/9999/groups")
        assert response.status_code == 200
        assert response.json() == []


class TestUserDataIntegrity:
    """Test user data integrity and validation."""

    def test_user_passwords_not_exposed(self, client, test_user):
        """Test that passwords are never exposed in responses."""
        response = client.get(f"/api/users/{test_user.id}")
        data = response.json()
        assert "password" not in data
        assert "password_hash" not in data

    def test_user_list_passwords_not_exposed(self, client, multiple_users):
        """Test that passwords are not exposed in user list."""
        response = client.get("/api/users/")
        users = response.json()
        for user in users:
            assert "password" not in user
            assert "password_hash" not in user
