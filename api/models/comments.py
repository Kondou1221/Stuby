from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DATETIME
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column, ForeignKey
from api.db import Base

class Comment(Base):
    __tablename__ = "COMMENTS"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USERS.user_id"), nullable=True)
    post_id = Column(Integer, ForeignKey("POSTS.post_id"), nullable=True)
    comment_sentence = Column(String(160))
    comment_img = Column(String(100))
    comment_create = Column(DATETIME, server_default=func.now(), nullable=False)
    mention_id = Column(Integer, ForeignKey("USERS.user_id"), nullable=True)

class Commentgood(Base):
    __tablename__ = "COMMENTGOODS"

    comment_id = Column(Integer, ForeignKey("COMMENTS.comment_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("USERS.user_id"), primary_key=True)