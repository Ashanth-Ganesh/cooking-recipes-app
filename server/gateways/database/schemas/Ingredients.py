from server.gateways.database.database import Base
from sqlalchemy import Column, Integer, String

class Ingredients(Base):
    __tablename__ = "Ingredients"

    ingredient_id = Column(Integer, primary_key=True, unique=True, index=True)
    ingredient_name = Column(String, unique=True, nullable=False)
    ingredient_type = Column(String, nullable=False)