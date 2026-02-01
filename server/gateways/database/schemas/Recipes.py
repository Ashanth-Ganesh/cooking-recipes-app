class Recipes(Base):
    __tablename__ = "FavoriteRecipes"

    recipe_id = Column(Integer, primary_key=True, unique=True)
    recipe_name = Column(String, unique=True, nullable=False)
    recipe_ingredients = Column(ARRAY(String), nullable=False)
    recipe_intolerances = Column(ARRAY(String), nullable=False)
    recipe_nutrition = Column(ARRAY(String), nullable=False)
    recipe_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(Users.user_id), nullable=False)