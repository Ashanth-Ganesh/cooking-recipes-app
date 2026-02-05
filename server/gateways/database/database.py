import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from schemas import Users, Recipes, Ingredients, CalendarEntries

Base = declarative_base()

class Database:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB")

        if not all([db_user, db_password, db_host, db_port, db_name]):
            raise ValueError("Missing database configuration in .env file")

        # Build connection string
        self.connection_string = (
            f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

        # Create engine
        self.engine = create_engine(self.connection_string, echo=True)

        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Create all tables if they don't exist
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Return a new SQLAlchemy session."""
        return self.SessionLocal()
    

    def add_user(self, username, email, password_hash):
        """Add a new user to the database."""
        session = self.get_session()
        try:
            new_user = Users(username=username, email=email, password_hash=password_hash)
            session.add(new_user)
            session.commit()
            return new_user.user_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_user(self, user_id, username=None, email=None, password_hash=None):
        """Update an existing user in the database."""
        session = self.get_session()
        try:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            if not user:
                raise ValueError(f"User with id {user_id} not found")
            
            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if password_hash is not None:
                user.password_hash = password_hash
            
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_user(self, user_id):
        """Remove a user from the database."""
        session = self.get_session()
        try:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            if not user:
                raise ValueError(f"User with id {user_id} not found")
            
            session.delete(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_recipe(self, recipe_name, recipe_ingredients, recipe_intolerances, recipe_nutrition, recipe_type, user_id):
        """Add a new recipe to the database."""
        session = self.get_session()
        try:
            new_recipe = Recipes(
                recipe_name=recipe_name,
                recipe_ingredients=recipe_ingredients,
                recipe_intolerances=recipe_intolerances,
                recipe_nutrition=recipe_nutrition,
                recipe_type=recipe_type,
                user_id=user_id
            )
            session.add(new_recipe)
            session.commit()
            return new_recipe.recipe_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_recipe(self, recipe_id, recipe_name=None, recipe_ingredients=None, recipe_intolerances=None, recipe_nutrition=None, recipe_type=None):
        """Update an existing recipe in the database."""
        session = self.get_session()
        try:
            recipe = session.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()
            if not recipe:
                raise ValueError(f"Recipe with id {recipe_id} not found")
            
            if recipe_name is not None:
                recipe.recipe_name = recipe_name
            if recipe_ingredients is not None:
                recipe.recipe_ingredients = recipe_ingredients
            if recipe_intolerances is not None:
                recipe.recipe_intolerances = recipe_intolerances
            if recipe_nutrition is not None:
                recipe.recipe_nutrition = recipe_nutrition
            if recipe_type is not None:
                recipe.recipe_type = recipe_type
            
            session.commit()
            return recipe
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_recipe(self, recipe_id):
        """Remove a recipe from the database."""
        session = self.get_session()
        try:
            recipe = session.query(Recipes).filter(Recipes.recipe_id == recipe_id).first()
            if not recipe:
                raise ValueError(f"Recipe with id {recipe_id} not found")
            
            session.delete(recipe)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_ingredient(self, ingredient_name, ingredient_type):
        """Add a new ingredient to the database."""
        session = self.get_session()
        try:
            new_ingredient = Ingredients(ingredient_name=ingredient_name, ingredient_type=ingredient_type)
            session.add(new_ingredient)
            session.commit()
            return new_ingredient.ingredient_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_ingredient(self, ingredient_id, ingredient_name=None, ingredient_type=None):
        """Update an existing ingredient in the database."""
        session = self.get_session()
        try:
            ingredient = session.query(Ingredients).filter(Ingredients.ingredient_id == ingredient_id).first()
            if not ingredient:
                raise ValueError(f"Ingredient with id {ingredient_id} not found")
            
            if ingredient_name is not None:
                ingredient.ingredient_name = ingredient_name
            if ingredient_type is not None:
                ingredient.ingredient_type = ingredient_type
            
            session.commit()
            return ingredient
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_ingredient(self, ingredient_id):
        """Remove an ingredient from the database."""
        session = self.get_session()
        try:
            ingredient = session.query(Ingredients).filter(Ingredients.ingredient_id == ingredient_id).first()
            if not ingredient:
                raise ValueError(f"Ingredient with id {ingredient_id} not found")
            
            session.delete(ingredient)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_calendar_entry(self, scheduled_date, scheduled_recipe_id, user_id):
        """Add a new calendar entry to the database."""
        session = self.get_session()
        try:
            new_entry = CalendarEntries(
                scheduled_date=scheduled_date,
                scheduled_recipe_id=scheduled_recipe_id,
                user_id=user_id
            )
            session.add(new_entry)
            session.commit()
            return new_entry.schedule_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_calendar_entry(self, schedule_id, scheduled_date=None, scheduled_recipe_id=None):
        """Update an existing calendar entry in the database."""
        session = self.get_session()
        try:
            entry = session.query(CalendarEntries).filter(CalendarEntries.schedule_id == schedule_id).first()
            if not entry:
                raise ValueError(f"Calendar entry with id {schedule_id} not found")
            
            if scheduled_date is not None:
                entry.scheduled_date = scheduled_date
            if scheduled_recipe_id is not None:
                entry.scheduled_recipe_id = scheduled_recipe_id
            
            session.commit()
            return entry
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_calendar_entry(self, schedule_id):
        """Remove a calendar entry from the database."""
        session = self.get_session()
        try:
            entry = session.query(CalendarEntries).filter(CalendarEntries.schedule_id == schedule_id).first()
            if not entry:
                raise ValueError(f"Calendar entry with id {schedule_id} not found")
            
            session.delete(entry)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()