import pytest
from app.models import Category


class TestListCategories:
    """Test list categories endpoint."""

    def test_list_categories_success(self, client, db):
        """Test listing all categories."""
        # Create test categories
        categories = [
            Category(name="Technology", icon="💻", color="#3B82F6", slug="technology"),
            Category(name="Sports", icon="⚽", color="#10B981", slug="sports"),
            Category(name="Arts", icon="🎨", color="#F59E0B", slug="arts"),
        ]
        for cat in categories:
            db.add(cat)
        db.commit()

        response = client.get("/api/categories/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("name" in cat for cat in data)
        assert all("icon" in cat for cat in data)

    def test_list_categories_empty(self, client):
        """Test listing categories when database is empty."""
        response = client.get("/api/categories/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_categories_structure(self, client, test_category):
        """Test category response structure."""
        response = client.get("/api/categories/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        category = data[0]
        assert "id" in category
        assert "name" in category
        assert "icon" in category
        assert "color" in category

    def test_list_categories_no_auth_required(self, client, test_category):
        """Test that categories endpoint doesn't require authentication."""
        response = client.get("/api/categories/")
        assert response.status_code == 200
        assert len(response.json()) >= 1
