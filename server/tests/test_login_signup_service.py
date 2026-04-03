"""
Unit tests for services/loginService.py and services/signupService.py.
The Database is mocked so no real database connection is needed.
"""
import pytest
from unittest.mock import MagicMock, patch
from services.authService import hash_password


# ─── loginService ────────────────────────────────────────────────────────────

class TestLoginUser:
    def test_returns_none_when_user_not_found(self):
        with patch("services.loginService.db") as mock_db:
            mock_db.get_user_by_username_or_email.return_value = None

            from services.loginService import login_user
            result = login_user("nobody", "password")

        assert result is None

    def test_returns_none_for_wrong_password(self):
        fake_user = MagicMock()
        fake_user.password_hash = hash_password("correct_password")

        with patch("services.loginService.db") as mock_db:
            mock_db.get_user_by_username_or_email.return_value = fake_user

            from services.loginService import login_user
            result = login_user("testuser", "wrong_password")

        assert result is None

    def test_returns_token_dict_for_valid_credentials(self):
        fake_user = MagicMock()
        fake_user.user_id = 1
        fake_user.username = "testuser"
        fake_user.email = "test@test.com"
        fake_user.role = "user"
        fake_user.password_hash = hash_password("secret")

        with patch("services.loginService.db") as mock_db:
            mock_db.get_user_by_username_or_email.return_value = fake_user

            from services.loginService import login_user
            result = login_user("testuser", "secret")

        assert result is not None
        assert "access_token" in result
        assert result["token_type"] == "bearer"
        assert result["user"]["username"] == "testuser"
        assert result["user"]["role"] == "user"

    def test_returned_token_is_decodable(self):
        from services.authService import decode_token

        fake_user = MagicMock()
        fake_user.user_id = 7
        fake_user.username = "chef_anna"
        fake_user.email = "anna@test.com"
        fake_user.role = "chef"
        fake_user.password_hash = hash_password("pass123")

        with patch("services.loginService.db") as mock_db:
            mock_db.get_user_by_username_or_email.return_value = fake_user

            from services.loginService import login_user
            result = login_user("chef_anna", "pass123")

        payload = decode_token(result["access_token"])
        assert payload["sub"] == "7"
        assert payload["role"] == "chef"


# ─── signupService ────────────────────────────────────────────────────────────

class TestSignupUser:
    def test_raises_value_error_when_username_taken(self):
        with patch("services.signupService.db") as mock_db:
            mock_db.get_user_by_username_or_email.return_value = MagicMock()

            from services.signupService import signup_user
            with pytest.raises(ValueError, match="Username already taken"):
                signup_user("existing", "new@test.com", "password")

    def test_raises_value_error_when_email_taken(self):
        # First call (username check) returns None, second call (email check) returns a user
        with patch("services.signupService.db") as mock_db:
            mock_db.get_user_by_username_or_email.side_effect = [None, MagicMock()]

            from services.signupService import signup_user
            with pytest.raises(ValueError, match="Email already registered"):
                signup_user("newuser", "taken@test.com", "password")

    def test_returns_token_dict_for_new_user(self):
        new_user = MagicMock()
        new_user.user_id = 5
        new_user.username = "brandnew"
        new_user.email = "brandnew@test.com"
        new_user.role = "user"

        with patch("services.signupService.db") as mock_db:
            mock_db.get_user_by_username_or_email.return_value = None
            mock_db.add_user.return_value = new_user

            from services.signupService import signup_user
            result = signup_user("brandnew", "brandnew@test.com", "password123")

        assert "access_token" in result
        assert result["token_type"] == "bearer"
        assert result["user"]["username"] == "brandnew"
        assert result["user"]["role"] == "user"

    def test_default_role_is_user(self):
        new_user = MagicMock()
        new_user.user_id = 6
        new_user.username = "plainuser"
        new_user.email = "plain@test.com"
        new_user.role = "user"

        with patch("services.signupService.db") as mock_db:
            mock_db.get_user_by_username_or_email.return_value = None
            mock_db.add_user.return_value = new_user

            from services.signupService import signup_user
            result = signup_user("plainuser", "plain@test.com", "password")

        assert result["user"]["role"] == "user"

    def test_chef_role_is_preserved(self):
        new_chef = MagicMock()
        new_chef.user_id = 8
        new_chef.username = "chefuser"
        new_chef.email = "chef@test.com"
        new_chef.role = "chef"

        with patch("services.signupService.db") as mock_db:
            mock_db.get_user_by_username_or_email.return_value = None
            mock_db.add_user.return_value = new_chef

            from services.signupService import signup_user
            result = signup_user("chefuser", "chef@test.com", "password", role="chef")

        assert result["user"]["role"] == "chef"
