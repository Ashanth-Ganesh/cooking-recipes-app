"""
Integration tests for routers/auth.py using FastAPI's TestClient.
External services (database, login/signup services) are mocked.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers.auth import router as auth_router
from services.authService import create_access_token, hash_password

app = FastAPI()
app.include_router(auth_router, prefix="/api/auth")
client = TestClient(app)


class TestSignupEndpoint:
    def test_successful_signup_returns_200(self):
        mock_result = {
            "access_token": "tok",
            "token_type": "bearer",
            "user": {"user_id": 1, "username": "alice", "email": "alice@test.com", "role": "user"},
        }
        with patch("routers.auth.signup_user", return_value=mock_result):
            response = client.post(
                "/api/auth/signup",
                json={"username": "alice", "email": "alice@test.com", "password": "secret1"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["username"] == "alice"
        assert "access_token" in data

    def test_duplicate_username_returns_400(self):
        with patch("routers.auth.signup_user", side_effect=ValueError("Username already taken")):
            response = client.post(
                "/api/auth/signup",
                json={"username": "existing", "email": "e@test.com", "password": "secret1"},
            )
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_duplicate_email_returns_400(self):
        with patch("routers.auth.signup_user", side_effect=ValueError("Email already registered")):
            response = client.post(
                "/api/auth/signup",
                json={"username": "newone", "email": "taken@test.com", "password": "secret1"},
            )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_missing_password_returns_422(self):
        response = client.post(
            "/api/auth/signup",
            json={"username": "alice", "email": "alice@test.com"},
        )
        assert response.status_code == 422

    def test_short_password_returns_422(self):
        # password min_length=6
        response = client.post(
            "/api/auth/signup",
            json={"username": "alice", "email": "alice@test.com", "password": "abc"},
        )
        assert response.status_code == 422


class TestLoginEndpoint:
    def test_successful_login_returns_200(self):
        mock_result = {
            "access_token": "valid-tok",
            "token_type": "bearer",
            "user": {"user_id": 1, "username": "alice", "email": "alice@test.com", "role": "user"},
        }
        with patch("routers.auth.login_user", return_value=mock_result):
            response = client.post(
                "/api/auth/login",
                json={"username_or_email": "alice", "password": "secret1"},
            )
        assert response.status_code == 200
        assert response.json()["access_token"] == "valid-tok"

    def test_invalid_credentials_returns_401(self):
        with patch("routers.auth.login_user", return_value=None):
            response = client.post(
                "/api/auth/login",
                json={"username_or_email": "alice", "password": "wrong"},
            )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_missing_fields_returns_422(self):
        response = client.post("/api/auth/login", json={"username_or_email": "alice"})
        assert response.status_code == 422


class TestGetMeEndpoint:
    def _make_token(self, user_id: int) -> str:
        return create_access_token({"sub": str(user_id)})

    def test_returns_user_data_with_valid_token(self):
        fake_user = MagicMock()
        fake_user.user_id = 1
        fake_user.username = "alice"
        fake_user.email = "alice@test.com"
        fake_user.role = "user"

        token = self._make_token(1)
        with patch("routers.auth.db") as mock_db:
            mock_db.get_user_by_id.return_value = fake_user
            response = client.get(
                "/api/auth/me",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "alice"
        assert data["email"] == "alice@test.com"

    def test_returns_401_without_token(self):
        response = client.get("/api/auth/me")
        assert response.status_code == 403  # HTTPBearer raises 403 when no credentials

    def test_returns_401_with_invalid_token(self):
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer this.is.fake"},
        )
        assert response.status_code == 401

    def test_returns_401_when_user_not_found_in_db(self):
        token = self._make_token(999)
        with patch("routers.auth.db") as mock_db:
            mock_db.get_user_by_id.return_value = None
            response = client.get(
                "/api/auth/me",
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 401
