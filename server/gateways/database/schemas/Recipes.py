from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from gateways.database.base import Base


class FavoriteRecipes(Base):
    __tablename__ = "FavoriteRecipes"

    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    spoonacular_id = Column(Integer, nullable=True)
    recipe_name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    ready_in_minutes = Column(Integer, nullable=True)
    servings = Column(Integer, nullable=True)
    is_custom = Column(Boolean, default=False)
    recipe_ingredients = Column(Text, nullable=True)  # JSON string for custom recipes
    recipe_instructions = Column(Text, nullable=True)
    recipe_type = Column(String, nullable=True)
    recipe_cuisine = Column(String, nullable=True)
