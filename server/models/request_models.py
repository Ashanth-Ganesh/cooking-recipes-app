from pydantic import BaseModel, EmailStr
from typing import Optional, List


class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


class SaveFavoriteRequest(BaseModel):
    spoonacular_id: int
    recipe_name: str
    image_url: Optional[str] = None
    ready_in_minutes: Optional[int] = None
    servings: Optional[int] = None
    recipe_type: Optional[str] = None
    recipe_cuisine: Optional[str] = None


class CustomRecipeRequest(BaseModel):
    recipe_name: str
    image_url: Optional[str] = None
    ready_in_minutes: Optional[int] = None
    servings: Optional[int] = None
    recipe_ingredients: List[str] = []
    recipe_instructions: str
    recipe_type: Optional[str] = None
    recipe_cuisine: Optional[str] = None
