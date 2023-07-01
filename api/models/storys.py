from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DATETIME
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column, ForeignKey
from api.db import Base

class Story(Base):
    __tablename__ = "STORYS"

    story_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USERS.user_id"), nullable=False)
    story_sentence = Column(String(100), nullable=False)
    story_title = Column(String(50), nullable=False)
    create_story = Column(DATETIME, server_default=func.now(), nullable=False)

class StoryGood(Base):
    __tablename__ = "STORYGOODS"

    story_id = Column(Integer, ForeignKey("STORYS.story_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("USERS.user_id"), primary_key=True)