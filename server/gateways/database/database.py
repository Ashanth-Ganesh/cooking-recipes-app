import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gateways.database.base import Base
from gateways.database.schemas.User import Users
from gateways.database.schemas.Recipes import FavoriteRecipes
from gateways.database.schemas.Ingredients import Ingredients
from gateways.database.schemas.CalendarEntries import CalendarEntries


class Database:
    def __init__(self):
        load_dotenv()

        db_user = os.getenv("POSTGRES_USER")
        db_password = os.getenv("POSTGRES_PASSWORD")
        db_host = os.getenv("POSTGRES_HOST", "localhost")
        db_port = os.getenv("POSTGRES_PORT", "5432")
        db_name = os.getenv("POSTGRES_DB")

        if not all([db_user, db_password, db_name]):
            raise ValueError("Missing database configuration in .env file")

        self.connection_string = (
            f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

        self.engine = create_engine(self.connection_string, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        """Create all tables if they don't exist."""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.SessionLocal()

    # ── Users ──────────────────────────────────────────────────────────────

    def add_user(self, username: str, email: str, password_hash: str, role: str = "user"):
        session = self.get_session()
        try:
            new_user = Users(username=username, email=email, password_hash=password_hash, role=role)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_user_by_id(self, user_id: int):
        session = self.get_session()
        try:
            return session.query(Users).filter(Users.user_id == user_id).first()
        finally:
            session.close()

    def get_user_by_username_or_email(self, identifier: str):
        session = self.get_session()
        try:
            return session.query(Users).filter(
                (Users.username == identifier) | (Users.email == identifier)
            ).first()
        finally:
            session.close()

    def update_user(self, user_id: int, username=None, email=None, password_hash=None):
        session = self.get_session()
        try:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
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

    def remove_user(self, user_id: int):
        session = self.get_session()
        try:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")
            session.delete(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # ── Favorites ──────────────────────────────────────────────────────────

    def get_favorites_by_user(self, user_id: int):
        session = self.get_session()
        try:
            return session.query(FavoriteRecipes).filter(FavoriteRecipes.user_id == user_id).all()
        finally:
            session.close()

    def add_favorite(self, user_id: int, spoonacular_id: int, recipe_name: str,
                     image_url=None, ready_in_minutes=None, servings=None,
                     recipe_type=None, recipe_cuisine=None):
        session = self.get_session()
        try:
            new_fav = FavoriteRecipes(
                user_id=user_id,
                spoonacular_id=spoonacular_id,
                recipe_name=recipe_name,
                image_url=image_url,
                ready_in_minutes=ready_in_minutes,
                servings=servings,
                is_custom=False,
                recipe_type=recipe_type,
                recipe_cuisine=recipe_cuisine,
            )
            session.add(new_fav)
            session.commit()
            session.refresh(new_fav)
            return new_fav
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_custom_recipe(self, user_id: int, recipe_name: str, image_url=None,
                          ready_in_minutes=None, servings=None, recipe_ingredients=None,
                          recipe_instructions=None, recipe_type=None, recipe_cuisine=None):
        session = self.get_session()
        try:
            new_recipe = FavoriteRecipes(
                user_id=user_id,
                spoonacular_id=None,
                recipe_name=recipe_name,
                image_url=image_url,
                ready_in_minutes=ready_in_minutes,
                servings=servings,
                is_custom=True,
                recipe_ingredients=json.dumps(recipe_ingredients or []),
                recipe_instructions=recipe_instructions,
                recipe_type=recipe_type,
                recipe_cuisine=recipe_cuisine,
            )
            session.add(new_recipe)
            session.commit()
            session.refresh(new_recipe)
            return new_recipe
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_all_custom_recipes(self):
        session = self.get_session()
        try:
            return session.query(FavoriteRecipes).filter(FavoriteRecipes.is_custom == True).all()
        finally:
            session.close()

    def get_custom_recipe_by_id(self, recipe_id: int):
        session = self.get_session()
        try:
            return session.query(FavoriteRecipes).filter(
                FavoriteRecipes.recipe_id == recipe_id,
                FavoriteRecipes.is_custom == True,
            ).first()
        finally:
            session.close()

    def remove_favorite(self, recipe_id: int, user_id: int):
        session = self.get_session()
        try:
            fav = session.query(FavoriteRecipes).filter(
                FavoriteRecipes.recipe_id == recipe_id,
                FavoriteRecipes.user_id == user_id
            ).first()
            if not fav:
                raise ValueError(f"Favorite {recipe_id} not found")
            session.delete(fav)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # ── Ingredients ────────────────────────────────────────────────────────

    def add_ingredient(self, ingredient_name: str, ingredient_type: str):
        session = self.get_session()
        try:
            new_ingredient = Ingredients(
                ingredient_name=ingredient_name, ingredient_type=ingredient_type
            )
            session.add(new_ingredient)
            session.commit()
            return new_ingredient.ingredient_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_ingredient(self, ingredient_id: int, ingredient_name=None, ingredient_type=None):
        session = self.get_session()
        try:
            ingredient = session.query(Ingredients).filter(
                Ingredients.ingredient_id == ingredient_id
            ).first()
            if not ingredient:
                raise ValueError(f"Ingredient {ingredient_id} not found")
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

    def remove_ingredient(self, ingredient_id: int):
        session = self.get_session()
        try:
            ingredient = session.query(Ingredients).filter(
                Ingredients.ingredient_id == ingredient_id
            ).first()
            if not ingredient:
                raise ValueError(f"Ingredient {ingredient_id} not found")
            session.delete(ingredient)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # ── Calendar ───────────────────────────────────────────────────────────

    def add_calendar_entry(self, scheduled_date, scheduled_recipe_id: int, user_id: int):
        session = self.get_session()
        try:
            new_entry = CalendarEntries(
                scheduled_date=scheduled_date,
                scheduled_recipe_id=scheduled_recipe_id,
                user_id=user_id,
            )
            session.add(new_entry)
            session.commit()
            return new_entry.schedule_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_calendar_entry(self, schedule_id: int, scheduled_date=None, scheduled_recipe_id=None):
        session = self.get_session()
        try:
            entry = session.query(CalendarEntries).filter(
                CalendarEntries.schedule_id == schedule_id
            ).first()
            if not entry:
                raise ValueError(f"Calendar entry {schedule_id} not found")
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

    def remove_calendar_entry(self, schedule_id: int):
        session = self.get_session()
        try:
            entry = session.query(CalendarEntries).filter(
                CalendarEntries.schedule_id == schedule_id
            ).first()
            if not entry:
                raise ValueError(f"Calendar entry {schedule_id} not found")
            session.delete(entry)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
