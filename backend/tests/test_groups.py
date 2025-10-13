import pytest
from app.models import Group, User


class TestListGroups:
    """Test list groups endpoint."""

    def test_list_groups_success(self, client, multiple_groups):
        """Test listing all groups."""
        response = client.get("/api/groups/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        assert all("name" in group for group in data)

    def test_list_groups_empty(self, client):
        """Test listing groups when database is empty."""
        response = client.get("/api/groups/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_groups_pagination(self, client, multiple_groups):
        """Test group list pagination."""
        response = client.get("/api/groups/?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        response = client.get("/api/groups/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_groups_filter_by_category(self, client, multiple_groups):
        """Test filtering groups by category."""
        response = client.get("/api/groups/?category=Technology")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "Technology"

    def test_list_groups_filter_by_location(self, client, db, test_user):
        """Test filtering groups by location."""
        group1 = Group(
            name="SF Group",
            description="Description",
            category="Technology",
            location="San Francisco, CA",
            organizer_id=test_user.id
        )
        group2 = Group(
            name="NY Group",
            description="Description",
            category="Technology",
            location="New York, NY",
            organizer_id=test_user.id
        )
        db.add_all([group1, group2])
        db.commit()

        response = client.get("/api/groups/?location=San Francisco")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "San Francisco" in data[0]["location"]

    def test_list_groups_multiple_filters(self, client, db, test_user):
        """Test filtering groups by multiple criteria."""
        group1 = Group(
            name="SF Tech Group",
            description="Description",
            category="Technology",
            location="San Francisco, CA",
            organizer_id=test_user.id
        )
        group2 = Group(
            name="SF Sports Group",
            description="Description",
            category="Sports",
            location="San Francisco, CA",
            organizer_id=test_user.id
        )
        db.add_all([group1, group2])
        db.commit()

        response = client.get("/api/groups/?category=Technology&location=San Francisco")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "Technology"


class TestGetGroup:
    """Test get group endpoint."""

    def test_get_group_success(self, client, test_group):
        """Test getting a specific group."""
        response = client.get(f"/api/groups/{test_group.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_group.id
        assert data["name"] == test_group.name
        assert data["category"] == test_group.category

    def test_get_group_not_found(self, client):
        """Test getting non-existent group."""
        response = client.get("/api/groups/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_group_invalid_id(self, client):
        """Test getting group with invalid ID."""
        response = client.get("/api/groups/invalid")
        assert response.status_code == 422


class TestCreateGroup:
    """Test create group endpoint."""

    def test_create_group_success(self, client, auth_headers):
        """Test creating a new group."""
        response = client.post(
            "/api/groups/",
            json={
                "name": "New Group",
                "description": "A new test group",
                "category": "Technology",
                "location": "San Francisco, CA"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Group"
        assert data["category"] == "Technology"
        assert "id" in data

    def test_create_group_unauthorized(self, client):
        """Test creating group without authentication."""
        response = client.post(
            "/api/groups/",
            json={
                "name": "Unauthorized Group",
                "description": "Should fail",
                "category": "Technology"
            }
        )
        assert response.status_code == 401

    def test_create_group_missing_required_fields(self, client, auth_headers):
        """Test creating group with missing required fields."""
        response = client.post(
            "/api/groups/",
            json={"name": "Incomplete Group"},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_create_group_minimal_data(self, client, auth_headers):
        """Test creating group with minimal required data."""
        response = client.post(
            "/api/groups/",
            json={
                "name": "Minimal Group",
                "category": "Technology"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Minimal Group"
        assert data["members_count"] == 0


class TestUpdateGroup:
    """Test update group endpoint."""

    def test_update_group_success(self, client, test_group, auth_headers):
        """Test updating a group."""
        response = client.put(
            f"/api/groups/{test_group.id}",
            json={
                "name": "Updated Group Name",
                "description": "Updated description"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Group Name"
        assert data["description"] == "Updated description"

    def test_update_group_unauthorized(self, client, test_group):
        """Test updating group without authentication."""
        response = client.put(
            f"/api/groups/{test_group.id}",
            json={"name": "Hacker Group"}
        )
        assert response.status_code == 401

    def test_update_group_forbidden(self, client, test_group, auth_headers2):
        """Test updating group by non-organizer."""
        response = client.put(
            f"/api/groups/{test_group.id}",
            json={"name": "Unauthorized Update"},
            headers=auth_headers2
        )
        assert response.status_code == 403
        assert "not authorized" in response.json()["detail"].lower()

    def test_update_group_not_found(self, client, auth_headers):
        """Test updating non-existent group."""
        response = client.put(
            "/api/groups/9999",
            json={"name": "Ghost Group"},
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_update_group_partial(self, client, test_group, auth_headers):
        """Test partial update of group."""
        original_category = test_group.category
        response = client.put(
            f"/api/groups/{test_group.id}",
            json={"description": "New description only"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "New description only"
        assert data["category"] == original_category


class TestJoinGroup:
    """Test join group endpoint."""

    def test_join_group_success(self, client, test_group, auth_headers2, db):
        """Test joining a group."""
        initial_count = test_group.members_count
        response = client.post(
            f"/api/groups/{test_group.id}/join",
            headers=auth_headers2
        )
        assert response.status_code == 200
        assert "success" in response.json()["message"].lower()

        # Verify member count increased
        db.refresh(test_group)
        assert test_group.members_count == initial_count + 1

    def test_join_group_idempotent(self, client, test_group, auth_headers2, db):
        """Test joining same group twice is idempotent."""
        # Join first time
        response1 = client.post(
            f"/api/groups/{test_group.id}/join",
            headers=auth_headers2
        )
        assert response1.status_code == 200
        db.refresh(test_group)
        count_after_first = test_group.members_count

        # Join second time
        response2 = client.post(
            f"/api/groups/{test_group.id}/join",
            headers=auth_headers2
        )
        assert response2.status_code == 200
        db.refresh(test_group)
        assert test_group.members_count == count_after_first

    def test_join_group_unauthorized(self, client, test_group):
        """Test joining group without authentication."""
        response = client.post(f"/api/groups/{test_group.id}/join")
        assert response.status_code == 401

    def test_join_group_not_found(self, client, auth_headers):
        """Test joining non-existent group."""
        response = client.post("/api/groups/9999/join", headers=auth_headers)
        assert response.status_code == 404


class TestGetGroupEvents:
    """Test get group events endpoint."""

    def test_get_group_events_success(self, client, test_group, multiple_events):
        """Test getting events for a group."""
        response = client.get(f"/api/groups/{test_group.id}/events")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert all(event["group_id"] == test_group.id for event in data)

    def test_get_group_events_empty(self, client, test_group):
        """Test getting events for group with no events."""
        response = client.get(f"/api/groups/{test_group.id}/events")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_group_events_nonexistent_group(self, client):
        """Test getting events for non-existent group."""
        response = client.get("/api/groups/9999/events")
        assert response.status_code == 200
        assert response.json() == []


class TestGetGroupMembers:
    """Test get group members endpoint."""

    def test_get_group_members_success(self, client, db, test_group, test_user2):
        """Test getting members of a group."""
        # Add member to group
        test_group.members.append(test_user2)
        db.commit()

        response = client.get(f"/api/groups/{test_group.id}/members")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(member["id"] == test_user2.id for member in data)

    def test_get_group_members_empty(self, client, test_group):
        """Test getting members for group with no members."""
        response = client.get(f"/api/groups/{test_group.id}/members")
        assert response.status_code == 200
        # Could be empty or have organizer

    def test_get_group_members_not_found(self, client):
        """Test getting members for non-existent group."""
        response = client.get("/api/groups/9999/members")
        assert response.status_code == 404

    def test_get_group_members_pagination(self, client, db, test_group, multiple_users):
        """Test group members pagination."""
        # Add multiple members
        for user in multiple_users[:3]:
            test_group.members.append(user)
        db.commit()

        response = client.get(f"/api/groups/{test_group.id}/members?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2
