from typing import Optional
from gateways.database.database import Database
from services.authService import verify_password, create_access_token
from services.shared.logger import logger

db = Database()


def login_user(username_or_email: str, password: str) -> Optional[dict]:
    user = db.get_user_by_username_or_email(username_or_email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None

    token = create_access_token({
        "sub": str(user.user_id),
        "username": user.username,
        "role": user.role,
    })
    logger.info(f"User '{user.username}' logged in")
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        },
    }
