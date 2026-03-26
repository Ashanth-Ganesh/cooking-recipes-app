from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.request_models import LoginRequest, SignupRequest
from services.loginService import login_user
from services.signupService import signup_user
from services.authService import decode_token
from gateways.database.database import Database
from gateways.database.schemas.User import Users

router = APIRouter(tags=["Authentication"])
security = HTTPBearer()
db = Database()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Users:
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.get_user_by_id(int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/signup")
def signup(request: SignupRequest):
    try:
        return signup_user(request.username, request.email, request.password, request.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(request: LoginRequest):
    result = login_user(request.username_or_email, request.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result


@router.get("/me")
def get_me(current_user: Users = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }
