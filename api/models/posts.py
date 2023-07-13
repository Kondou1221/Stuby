from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DATETIME
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column, ForeignKey
from api.db import Base


class Post(Base):
    __tablename__ = "POSTS"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USERS.user_id"), nullable=False )
    post_sentence = Column(String(160), nullable=True)
    post_img = Column(String(25), nullable=True)
    post_create = Column(DATETIME, server_default=func.now(), nullable=False)

class Postgood(Base):
    __tablename__ = "POSTGOODS"

    user_id = Column(Integer, ForeignKey("USERS.user_id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("POSTS.post_id"), primary_key=True)
