from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DATETIME
from sqlalchemy.sql.schema import Column, ForeignKey
from api.db import Base

class Comment(Base):
    __tablename__ = "COMMENTS"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USERS.user_id"), nullable=True)
    post_id = Column(Integer, ForeignKey("POSTS.post_id"), nullable=True)
    comment_sentence = Column(String(160))
    comment_create = Column(DATETIME, nullable=False)
    mention_id = Column(Integer, ForeignKey("USERS.user_id"))

class Commentgood(Base):
    __tablename__ = "COMMENTGOODS"

    comment_good_id = Column(Integer, primary_key=True, autoincrement=True)
    comment_id = Column(Integer, ForeignKey("COMMENTS.comment_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("USERS.user_id"), nullable=False)