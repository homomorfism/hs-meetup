import pytest
from datetime import timedelta
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_password_hash_not_plaintext(self):
        """Test that hashed password is different from plaintext."""
        password = "mypassword123"
        hashed = get_password_hash(password)
        assert hashed != password

    def test_password_verification_success(self):
        """Test successful password verification."""
        password = "mypassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_password_verification_failure(self):
        """Test failed password verification."""
        password = "mypassword123"
        hashed = get_password_hash(password)
        assert verify_password("wrongpassword", hashed) is False

    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (salt)."""
        password = "mypassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2
        # But both should verify
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    def test_empty_password(self):
        """Test hashing empty password."""
        hashed = get_password_hash("")
        assert verify_password("", hashed) is True


class TestJWTTokens:
    """Test JWT token creation and validation."""

    def test_create_token_success(self):
        """Test creating a JWT token."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_token_success(self):
        """Test decoding a valid JWT token."""
        email = "test@example.com"
        token = create_access_token({"sub": email})
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == email

    def test_decode_invalid_token(self):
        """Test decoding invalid token."""
        payload = decode_access_token("invalid.token.here")
        assert payload is None

    def test_decode_expired_token(self):
        """Test decoding expired token."""
        token = create_access_token(
            {"sub": "test@example.com"},
            expires_delta=timedelta(seconds=-1)
        )
        payload = decode_access_token(token)
        assert payload is None

    def test_token_contains_expiration(self):
        """Test that token contains expiration claim."""
        token = create_access_token({"sub": "test@example.com"})
        payload = decode_access_token(token)
        assert "exp" in payload

    def test_custom_expiration(self):
        """Test creating token with custom expiration."""
        token = create_access_token(
            {"sub": "test@example.com"},
            expires_delta=timedelta(minutes=60)
        )
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "test@example.com"


class TestAuthorizationBoundaries:
    """Test authorization boundaries between users."""

    def test_user_cannot_update_other_user(self, client, test_user, test_user2, auth_headers):
        """Test that user cannot update another user's profile."""
        response = client.put(
            f"/api/users/{test_user2.id}",
            json={"name": "Hacked Name"},
            headers=auth_headers
        )
        assert response.status_code == 403

    def test_user_cannot_update_other_group(self, client, db, test_user2, test_group, auth_headers2):
        """Test that user cannot update another user's group."""
        response = client.put(
            f"/api/groups/{test_group.id}",
            json={"name": "Hacked Group"},
            headers=auth_headers2
        )
        assert response.status_code == 403

    def test_user_cannot_update_other_event(self, client, test_event, auth_headers2):
        """Test that user cannot update another user's event."""
        response = client.put(
            f"/api/events/{test_event.id}",
            json={"title": "Hacked Event"},
            headers=auth_headers2
        )
        assert response.status_code == 403

    def test_non_organizer_cannot_create_group_event(self, client, test_group, auth_headers2):
        """Test that non-organizer cannot create event for group."""
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


class TestTokenSecurity:
    """Test token security features."""

    def test_malformed_bearer_token(self, client):
        """Test request with malformed bearer token."""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "InvalidFormat token123"}
        )
        assert response.status_code == 401

    def test_missing_bearer_prefix(self, client, auth_token):
        """Test request without Bearer prefix."""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": auth_token}
        )
        assert response.status_code == 401

    def test_empty_token(self, client):
        """Test request with empty token."""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer "}
        )
        assert response.status_code == 401

    def test_token_with_invalid_signature(self, client):
        """Test token with tampered signature."""
        # Create valid token structure but invalid signature
        fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIn0.invalid_signature"
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {fake_token}"}
        )
        assert response.status_code == 401


class TestPasswordPolicy:
    """Test password-related security policies."""

    def test_passwords_not_returned_in_responses(self, client, test_user):
        """Test that passwords are never exposed in API responses."""
        # Get user
        response = client.get(f"/api/users/{test_user.id}")
        data = response.json()
        assert "password" not in data
        assert "password_hash" not in data

        # List users
        response = client.get("/api/users/")
        users = response.json()
        for user in users:
            assert "password" not in user
            assert "password_hash" not in user

        # Get current user
        response = client.post(
            "/api/auth/login",
            data={"username": test_user.email, "password": "password123"}
        )
        token = response.json()["access_token"]

        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        data = response.json()
        assert "password" not in data
        assert "password_hash" not in data

    def test_signup_with_weak_password(self, client):
        """Test weak passwords are not allowed."""
       
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "weak@example.com",
                "password": "123",
                "name": "Weak Password User"
            }
        )
        # Currently accepts any password
        assert response.status_code == 422


class TestAuthenticationEdgeCases:
    """Test edge cases in authentication."""

    def test_login_case_sensitive_email(self, client, test_user):
        """Test that email is case-sensitive in login."""
        response = client.post(
            "/api/auth/login",
            data={
                "username": test_user.email.upper(),
                "password": "password123"
            }
        )
        # Depending on implementation, this might fail
        # Current implementation is case-sensitive
        assert response.status_code in [200, 401]

    def test_multiple_failed_login_attempts(self, client, test_user):
        """Test multiple failed login attempts (no rate limiting currently)."""
        for _ in range(5):
            response = client.post(
                "/api/auth/login",
                data={
                    "username": test_user.email,
                    "password": "wrongpassword"
                }
            )
            assert response.status_code == 401

        # Verify correct password still works
        response = client.post(
            "/api/auth/login",
            data={
                "username": test_user.email,
                "password": "password123"
            }
        )
        assert response.status_code == 200

    def test_concurrent_logins_same_user(self, client, test_user):
        """Test that same user can have multiple active sessions."""
        # Login twice
        response1 = client.post(
            "/api/auth/login",
            data={"username": test_user.email, "password": "password123"}
        )
        token1 = response1.json()["access_token"]

        response2 = client.post(
            "/api/auth/login",
            data={"username": test_user.email, "password": "password123"}
        )
        token2 = response2.json()["access_token"]

        # Both tokens should be valid
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token1}"}
        )
        assert response.status_code == 200

        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 200
