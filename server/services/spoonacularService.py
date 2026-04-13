import os
from typing import Optional
import httpx
from dotenv import load_dotenv
from services.shared.logger import logger

load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY", "")
BASE_URL = "https://api.spoonacular.com"


async def search_recipes(
    query: str = "",
    cuisine: str = "",
    diet: str = "",
    intolerances: str = "",
    meal_type: str = "",
    max_ready_time: Optional[int] = None,
    include_ingredients: str = "",
    number: int = 12,
    offset: int = 0,
) -> dict:
    params: dict = {
        "apiKey": SPOONACULAR_API_KEY,
        "addRecipeInformation": "true",
        "fillIngredients": "true",
        "number": number,
        "offset": offset,
    }
    if query:
        params["query"] = query
    if cuisine:
        params["cuisine"] = cuisine
    if diet:
        params["diet"] = diet
    if intolerances:
        params["intolerances"] = intolerances
    if meal_type:
        params["type"] = meal_type
    if max_ready_time:
        params["maxReadyTime"] = max_ready_time
    if include_ingredients:
        params["includeIngredients"] = include_ingredients

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(f"{BASE_URL}/recipes/complexSearch", params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Spoonacular search: {data.get('totalResults', 0)} results for '{query}'")
        return data


async def get_recipe_detail(recipe_id: int) -> dict:
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "includeNutrition": "true",
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(f"{BASE_URL}/recipes/{recipe_id}/information", params=params)
        response.raise_for_status()
        return response.json()


async def find_by_ingredients(ingredients: str, number: int = 12) -> list:
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "ingredients": ingredients,
        "number": number,
        "ranking": 1,
        "ignorePantry": "true",
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(f"{BASE_URL}/recipes/findByIngredients", params=params)
        response.raise_for_status()
        return response.json()
