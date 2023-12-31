from sqlalchemy.types import Integer
from sqlalchemy.sql.schema import Column, ForeignKey

from api.db import Base

class Follow(Base):
    __tablename__ = "FOLLOWS"

    follow_id = Column(Integer, ForeignKey("USERS.user_id"), primary_key=True)
    follower_id = Column(Integer, ForeignKey("USERS.user_id"), primary_key=True)