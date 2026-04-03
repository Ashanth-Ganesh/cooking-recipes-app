"""
Integration tests for routers/favorites.py using FastAPI's TestClient.
The Database is mocked to avoid requiring a real PostgreSQL connection.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers.favorites import router as favorites_router
from services.authService import create_access_token

app = FastAPI()
app.include_router(favorites_router, prefix="/api/favorites")
client = TestClient(app)


def _auth_headers(user_id: int = 1) -> dict:
    token = create_access_token({"sub": str(user_id)})
    return {"Authorization": f"Bearer {token}"}


def _make_fake_user(role: str = "user") -> MagicMock:
    user = MagicMock()
    user.user_id = 1
    user.username = "testuser"
    user.role = role
    return user


def _make_fake_favorite() -> MagicMock:
    fav = MagicMock()
    fav.recipe_id = 10
    fav.spoonacular_id = 42
    fav.recipe_name = "Pasta"
    fav.image_url = "https://img.example.com/pasta.jpg"
    fav.ready_in_minutes = 30
    fav.servings = 2
    fav.is_custom = False
    fav.recipe_type = "main course"
    fav.recipe_cuisine = "Italian"
    return fav


class TestGetFavorites:
    def test_returns_favorites_for_authenticated_user(self):
        fake_fav = _make_fake_favorite()
        with patch("routers.favorites.db") as mock_db:
            mock_db.get_user_by_id.return_value = _make_fake_user()
            mock_db.get_favorites_by_user.return_value = [fake_fav]
            response = client.get("/api/favorites", headers=_auth_headers())

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["recipe_name"] == "Pasta"
        assert data[0]["spoonacular_id"] == 42

    def test_returns_empty_list_when_no_favorites(self):
        with patch("routers.favorites.db") as mock_db:
            mock_db.get_user_by_id.return_value = _make_fake_user()
            mock_db.get_favorites_by_user.return_value = []
            response = client.get("/api/favorites", headers=_auth_headers())

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_403_without_token(self):
        response = client.get("/api/favorites")
        assert response.status_code == 403


class TestSaveFavorite:
    def test_saves_recipe_successfully(self):
        fake_fav = _make_fake_favorite()
        fake_fav.recipe_id = 10

        with patch("routers.favorites.db") as mock_db:
            mock_db.get_user_by_id.return_value = _make_fake_user()
            mock_db.get_favorites_by_user.return_value = []
            mock_db.add_favorite.return_value = fake_fav

            response = client.post(
                "/api/favorites",
                json={
                    "spoonacular_id": 42,
                    "recipe_name": "Pasta",
                    "image_url": "https://img.example.com/pasta.jpg",
                    "ready_in_minutes": 30,
                    "servings": 2,
                },
                headers=_auth_headers(),
            )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Recipe saved to favorites"
        assert data["recipe_id"] == 10

    def test_returns_400_when_recipe_already_saved(self):
        fake_fav = _make_fake_favorite()

        with patch("routers.favorites.db") as mock_db:
            mock_db.get_user_by_id.return_value = _make_fake_user()
            mock_db.get_favorites_by_user.return_value = [fake_fav]

            response = client.post(
                "/api/favorites",
                json={"spoonacular_id": 42, "recipe_name": "Pasta"},
                headers=_auth_headers(),
            )

        assert response.status_code == 400
        assert "already in favorites" in response.json()["detail"]

    def test_returns_403_without_token(self):
        response = client.post(
            "/api/favorites",
            json={"spoonacular_id": 1, "recipe_name": "Test"},
        )
        assert response.status_code == 403


class TestRemoveFavorite:
    def test_removes_recipe_successfully(self):
        with patch("routers.favorites.db") as mock_db:
            mock_db.get_user_by_id.return_value = _make_fake_user()
            mock_db.remove_favorite.return_value = None

            response = client.delete("/api/favorites/10", headers=_auth_headers())

        assert response.status_code == 200
        assert response.json()["message"] == "Recipe removed from favorites"

    def test_returns_404_when_favorite_not_found(self):
        with patch("routers.favorites.db") as mock_db:
            mock_db.get_user_by_id.return_value = _make_fake_user()
            mock_db.remove_favorite.side_effect = ValueError("not found")

            response = client.delete("/api/favorites/999", headers=_auth_headers())

        assert response.status_code == 404

    def test_returns_403_without_token(self):
        response = client.delete("/api/favorites/10")
        assert response.status_code == 403


class TestAddCustomRecipe:
    def test_chef_can_add_custom_recipe(self):
        new_recipe = MagicMock()
        new_recipe.recipe_id = 55

        with patch("routers.favorites.db") as mock_db:
            mock_db.get_user_by_id.return_value = _make_fake_user(role="chef")
            mock_db.add_custom_recipe.return_value = new_recipe

            response = client.post(
                "/api/favorites/custom",
                json={
                    "recipe_name": "Chef's Special",
                    "recipe_instructions": "Cook with love.",
                    "recipe_ingredients": ["garlic", "olive oil"],
                },
                headers=_auth_headers(),
            )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Custom recipe added"
        assert data["recipe_id"] == 55

    def test_admin_can_add_custom_recipe(self):
        new_recipe = MagicMock()
        new_recipe.recipe_id = 56

        with patch("routers.favorites.db") as mock_db:
            mock_db.get_user_by_id.return_value = _make_fake_user(role="admin")
            mock_db.add_custom_recipe.return_value = new_recipe

            response = client.post(
                "/api/favorites/custom",
                json={"recipe_name": "Admin Dish", "recipe_instructions": "Instructions here."},
                headers=_auth_headers(),
            )

        assert response.status_code == 200

    def test_regular_user_cannot_add_custom_recipe(self):
        with patch("routers.favorites.db") as mock_db:
            mock_db.get_user_by_id.return_value = _make_fake_user(role="user")

            response = client.post(
                "/api/favorites/custom",
                json={"recipe_name": "My Dish", "recipe_instructions": "Cook it."},
                headers=_auth_headers(),
            )

        assert response.status_code == 403
        assert "Only chefs and admins" in response.json()["detail"]

    def test_returns_403_without_token(self):
        response = client.post(
            "/api/favorites/custom",
            json={"recipe_name": "My Dish", "recipe_instructions": "Cook it."},
        )
        assert response.status_code == 403
