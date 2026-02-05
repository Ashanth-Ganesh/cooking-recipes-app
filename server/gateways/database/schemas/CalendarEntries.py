from server.gateways.database.database import Base
from sqlalchemy import Column, Integer, Date, ForeignKey
from server.gateways.database.schemas.Recipes import Recipes
from server.gateways.database.schemas.User import Users

class CalendarEntries(Base):
    __tablename__ = "Calendar"

    schedule_id = Column(Integer, primary_key=True, unique=True, index=True)
    scheduled_date = Column(Date, nullable=False)
    scheduled_recipe_id = Column(Integer, ForeignKey(Recipes.recipe_id), nullable=False)
    user_id = Column(Integer, ForeignKey(Users.user_id), nullable=False)