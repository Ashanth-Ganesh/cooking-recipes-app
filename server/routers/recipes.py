from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from services.spoonacularService import search_recipes, get_recipe_detail, find_by_ingredients

router = APIRouter(tags=["Recipes"])


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
    try:
        return await get_recipe_detail(recipe_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Recipe not found")
