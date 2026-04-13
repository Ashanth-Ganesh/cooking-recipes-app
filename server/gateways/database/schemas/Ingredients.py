from sqlalchemy import Column, Integer, String
from gateways.database.base import Base


class Ingredients(Base):
    __tablename__ = "Ingredients"

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ingredient_name = Column(String, unique=True, nullable=False)
    ingredient_type = Column(String, nullable=False)
