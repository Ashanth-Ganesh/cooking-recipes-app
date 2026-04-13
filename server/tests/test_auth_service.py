"""
Unit tests for services/authService.py — password hashing and JWT utilities.
No database or network calls are made here.
"""
import pytest
from services.authService import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)


class TestHashPassword:
    def test_returns_a_string(self):
        result = hash_password("mypassword")
        assert isinstance(result, str)

    def test_hashed_value_differs_from_plain(self):
        plain = "mypassword"
        assert hash_password(plain) != plain

    def test_two_hashes_of_same_password_differ(self):
        # bcrypt uses a random salt each time
        h1 = hash_password("samepassword")
        h2 = hash_password("samepassword")
        assert h1 != h2


class TestVerifyPassword:
    def test_returns_true_for_correct_password(self):
        hashed = hash_password("correct")
        assert verify_password("correct", hashed) is True

    def test_returns_false_for_wrong_password(self):
        hashed = hash_password("correct")
        assert verify_password("wrong", hashed) is False

    def test_returns_false_for_empty_password(self):
        hashed = hash_password("notempty")
        assert verify_password("", hashed) is False


class TestCreateAccessToken:
    def test_returns_a_string(self):
        token = create_access_token({"sub": "1"})
        assert isinstance(token, str)

    def test_token_is_non_empty(self):
        token = create_access_token({"sub": "1"})
        assert len(token) > 0

    def test_different_data_produces_different_tokens(self):
        t1 = create_access_token({"sub": "1"})
        t2 = create_access_token({"sub": "2"})
        assert t1 != t2


class TestDecodeToken:
    def test_returns_payload_for_valid_token(self):
        token = create_access_token({"sub": "42", "role": "user"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "42"
        assert payload["role"] == "user"

    def test_returns_none_for_invalid_token(self):
        result = decode_token("this.is.not.valid")
        assert result is None

    def test_returns_none_for_empty_string(self):
        result = decode_token("")
        assert result is None

    def test_returns_none_for_tampered_token(self):
        token = create_access_token({"sub": "1"})
        tampered = token[:-5] + "XXXXX"
        assert decode_token(tampered) is None

    def test_roundtrip_preserves_all_claims(self):
        data = {"sub": "99", "username": "chef_mario", "role": "chef"}
        token = create_access_token(data)
        payload = decode_token(token)
        assert payload["sub"] == "99"
        assert payload["username"] == "chef_mario"
        assert payload["role"] == "chef"
