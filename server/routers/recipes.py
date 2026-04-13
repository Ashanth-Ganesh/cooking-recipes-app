from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from services.spoonacularService import search_recipes, get_recipe_detail, find_by_ingredients
from gateways.database.database import Database

router = APIRouter(tags=["Recipes"])
db = Database()


@router.get("/search")
async def search(
    query: Optional[str] = Query(default=""),
    cuisine: Optional[str] = Query(default=""),
    diet: Optional[str] = Query(default=""),
    intolerances: Optional[str] = Query(default=""),
    meal_type: Optional[str] = Query(default=""),
    max_ready_time: Optional[int] = Query(default=None),
    ingredients: Optional[str] = Query(default=""),
    number: int = Query(default=12, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    try:
        return await search_recipes(
            query=query or "",
            cuisine=cuisine or "",
            diet=diet or "",
            intolerances=intolerances or "",
            meal_type=meal_type or "",
            max_ready_time=max_ready_time,
            include_ingredients=ingredients or "",
            number=number,
            offset=offset,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Spoonacular API error: {str(e)}")


@router.get("/custom")
async def get_custom_recipes():
    recipes = db.get_all_custom_recipes()
    results = [
        {
            "id": r.recipe_id,
            "title": r.recipe_name,
            "image": r.image_url or "",
            "readyInMinutes": r.ready_in_minutes,
            "servings": r.servings,
            "cuisines": [r.recipe_cuisine] if r.recipe_cuisine else [],
            "dishTypes": [r.recipe_type] if r.recipe_type else [],
            "is_custom": True,
        }
        for r in recipes
    ]
    return {"results": results, "offset": 0, "number": len(results), "totalResults": len(results)}


@router.get("/by-ingredients")
async def by_ingredients(
    ingredients: str = Query(..., description="Comma-separated ingredient list"),
    number: int = Query(default=12, ge=1, le=100),
):
    try:
        return await find_by_ingredients(ingredients, number)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Spoonacular API error: {str(e)}")


@router.get("/{recipe_id}")
async def get_recipe(recipe_id: int):
    custom = db.get_custom_recipe_by_id(recipe_id)
    if custom:
        import json as _json
        try:
            ingredients = _json.loads(custom.recipe_ingredients or "[]")
        except Exception:
            ingredients = []
        return {
            "id": custom.recipe_id,
            "title": custom.recipe_name,
            "image": custom.image_url or "",
            "readyInMinutes": custom.ready_in_minutes,
            "servings": custom.servings,
            "cuisines": [custom.recipe_cuisine] if custom.recipe_cuisine else [],
            "dishTypes": [custom.recipe_type] if custom.recipe_type else [],
            "instructions": custom.recipe_instructions or "",
            "extendedIngredients": [
                {"id": i, "name": ing, "original": ing, "amount": 0, "unit": ""}
                for i, ing in enumerate(ingredients)
            ],
            "is_custom": True,
        }
    try:
        return await get_recipe_detail(recipe_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Recipe not found")
