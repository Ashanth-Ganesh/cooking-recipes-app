from pydantic import BaseModel, EmailStr

class SignUpRequest(BaseModel):
    username: str
    password: str
    password_repeat: str
    email: EmailStr
    role: str

def validate_request(request: SignUpRequest):
    if request.password != request.password_repeat:
        raise ValueError("password: \"{request.password}\" and password_repeat: \"{request.password_repeat}\" do not match!")
    
    return {"username": request.username, "role": request.role}