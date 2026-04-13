from gateways.database.database import Database
from services.authService import hash_password, create_access_token
from services.shared.logger import logger

db = Database()


def signup_user(username: str, email: str, password: str, role: str = "user") -> dict:
    existing = db.get_user_by_username_or_email(username)
    if existing:
        raise ValueError("Username already taken")

    existing_email = db.get_user_by_username_or_email(email)
    if existing_email:
        raise ValueError("Email already registered")

    password_hash = hash_password(password)
    new_user = db.add_user(username=username, email=email, password_hash=password_hash, role=role)

    token = create_access_token({
        "sub": str(new_user.user_id),
        "username": new_user.username,
        "role": new_user.role,
    })
    logger.info(f"New user '{username}' registered with role '{role}'")
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": new_user.user_id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role,
        },
    }
