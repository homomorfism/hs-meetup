import pytest
from datetime import timedelta
from app.core.security import create_access_token
from app.models import User


class TestSignup:
    """Test user signup endpoint."""

    def test_signup_success(self, client):
        """Test successful user signup."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "password123",
                "name": "New User",
                "location": "Barcelona",
                "bio": "Test bio"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["name"] == "New User"
        assert data["location"] == "San Francisco"
        assert "password" not in data
        assert "password_hash" not in data
        assert "id" in data

    def test_signup_duplicate_email(self, client, test_user):
        """Test signup with duplicate email."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": test_user.email,
                "password": "password123",
                "name": "New User",
                "location": "San Francisco"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_signup_missing_required_fields(self, client):
        """Test signup with missing required fields."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 422

    def test_signup_invalid_email(self, client):
        """Test signup with invalid email format."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "invalid-email",
                "password": "password123",
                "name": "New User"
            }
        )
        assert response.status_code == 422

    def test_signup_minimal_data(self, client):
        """Test signup with minimal required data."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "minimal@example.com",
                "password": "password123",
                "name": "Minimal User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "minimal@example.com"
        assert data["name"] == "Minimal User"


class TestLogin:
    """Test user login endpoint."""

    def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post(
            "/api/auth/login",
            data={
                "username": test_user.email,
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password."""
        response = client.post(
            "/api/auth/login",
            data={
                "username": test_user.email,
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 401

    def test_login_missing_credentials(self, client):
        """Test login with missing credentials."""
        response = client.post("/api/auth/login", data={})
        assert response.status_code == 422

    def test_login_empty_password(self, client, test_user):
        """Test login with empty password."""
        response = client.post(
            "/api/auth/login",
            data={
                "username": test_user.email,
                "password": ""
            }
        )
        assert response.status_code == 401


class TestGetCurrentUser:
    """Test get current user endpoint."""

    def test_get_current_user_success(self, client, test_user, auth_headers):
        """Test getting current user with valid token."""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["name"] == test_user.name
        assert data["id"] == test_user.id

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token."""
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_get_current_user_expired_token(self, client, test_user):
        """Test getting current user with expired token."""
        # Create expired token
        expired_token = create_access_token(
            data={"sub": test_user.email},
            expires_delta=timedelta(seconds=-1)
        )
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401

    def test_get_current_user_malformed_token(self, client):
        """Test getting current user with malformed token."""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "InvalidBearer token"}
        )
        assert response.status_code == 401


class TestAuthenticationFlow:
    """Test complete authentication flow."""

    def test_signup_login_flow(self, client):
        """Test signup followed by login."""
        # Signup
        signup_response = client.post(
            "/api/auth/signup",
            json={
                "email": "flowtest@example.com",
                "password": "password123",
                "name": "Flow Test"
            }
        )
        assert signup_response.status_code == 201

        # Login
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "flowtest@example.com",
                "password": "password123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Access protected endpoint
        me_response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "flowtest@example.com"
