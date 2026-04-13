from sqlalchemy import Column, Integer, String
from gateways.database.base import Base


class Users(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
