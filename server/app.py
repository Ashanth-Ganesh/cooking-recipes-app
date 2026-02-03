from fastapi import FastAPI
from services import signupService

app = FastAPI()

@app.get("/signup")
def sign_up(request: signupService.SignUpRequest):
    return signupService.validate_request(request)

