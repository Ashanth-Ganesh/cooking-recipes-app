from sqlalchemy import Column, Integer, Date, ForeignKey
from gateways.database.base import Base


class CalendarEntries(Base):
    __tablename__ = "Calendar"

    schedule_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    scheduled_date = Column(Date, nullable=False)
    scheduled_recipe_id = Column(Integer, ForeignKey("FavoriteRecipes.recipe_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
