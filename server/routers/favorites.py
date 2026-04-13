from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.request_models import SaveFavoriteRequest, CustomRecipeRequest
from services.authService import decode_token
from gateways.database.database import Database
from gateways.database.schemas.User import Users

router = APIRouter(tags=["Favorites"])
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


@router.get("")
def get_favorites(current_user: Users = Depends(get_current_user)):
    favorites = db.get_favorites_by_user(current_user.user_id)
    return [
        {
            "recipe_id": f.recipe_id,
            "spoonacular_id": f.spoonacular_id,
            "recipe_name": f.recipe_name,
            "image_url": f.image_url,
            "ready_in_minutes": f.ready_in_minutes,
            "servings": f.servings,
            "is_custom": f.is_custom,
            "recipe_type": f.recipe_type,
            "recipe_cuisine": f.recipe_cuisine,
        }
        for f in favorites
    ]


@router.post("")
def save_favorite(request: SaveFavoriteRequest, current_user: Users = Depends(get_current_user)):
    favorites = db.get_favorites_by_user(current_user.user_id)
    already_saved = any(f.spoonacular_id == request.spoonacular_id for f in favorites)
    if already_saved:
        raise HTTPException(status_code=400, detail="Recipe already in favorites")

    fav = db.add_favorite(
        user_id=current_user.user_id,
        spoonacular_id=request.spoonacular_id,
        recipe_name=request.recipe_name,
        image_url=request.image_url,
        ready_in_minutes=request.ready_in_minutes,
        servings=request.servings,
        recipe_type=request.recipe_type,
        recipe_cuisine=request.recipe_cuisine,
    )
    return {"message": "Recipe saved to favorites", "recipe_id": fav.recipe_id}


@router.delete("/{recipe_id}")
def remove_favorite(recipe_id: int, current_user: Users = Depends(get_current_user)):
    try:
        db.remove_favorite(recipe_id, current_user.user_id)
        return {"message": "Recipe removed from favorites"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Favorite not found")


@router.post("/custom")
def add_custom_recipe(
    request: CustomRecipeRequest,
    current_user: Users = Depends(get_current_user),
):
    if current_user.role not in ["chef", "admin"]:
        raise HTTPException(status_code=403, detail="Only chefs and admins can add custom recipes")

    recipe = db.add_custom_recipe(
        user_id=current_user.user_id,
        recipe_name=request.recipe_name,
        image_url=request.image_url,
        ready_in_minutes=request.ready_in_minutes,
        servings=request.servings,
        recipe_ingredients=request.recipe_ingredients,
        recipe_instructions=request.recipe_instructions,
        recipe_type=request.recipe_type,
        recipe_cuisine=request.recipe_cuisine,
    )
    return {"message": "Custom recipe added", "recipe_id": recipe.recipe_id}
