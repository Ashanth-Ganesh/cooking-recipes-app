from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

# login endpoint
@app.post('http://localhost:8000/login')
async def login(credentials: LoginRequest):
    # Check username and password (simplified example)
    if credentials.email == "admin" and credentials.password == "secret123":
        return {
            "message": "Login successful",
            "token": "some_jwt_token_here"
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")