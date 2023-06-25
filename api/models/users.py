from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.sql.schema import Column, ForeignKey

from api.db import Base

class Gender(Base):
    __tablename__ = "GENDER" #テーブルの名前

    type = Column(String(5), primary_key=True, nullable=False)

class Usergood(Base):
    __tablename__ = "USERGOODS"

    liked_user_id = Column(Integer, ForeignKey("USERS.user_id"), primary_key=True)
    like_user_id = Column(Integer, ForeignKey("USERS.user_id"), primary_key=True)


class User(Base):
    __tablename__ = "USERS" #テーブルの名前

    #テーブルのカラム
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(25), nullable=False)
    user_email = Column(String(50), nullable=False)
    user_passwd = Column(String(45), nullable=False)
    user_gender = Column(String(4), ForeignKey("GENDER.type"), nullable=False)
    user_old = Column(Integer, nullable=False)
    user_school_name = Column(String(255), nullable=False)
    user_faculty = Column(String(50), nullable=False)
    user_schoolyear = Column(Integer, nullable=False)
    fasubject = Column(String(25), nullable=False)
    wesubject = Column(String(25), nullable=False)
    icon_img = Column(String(25))
    pro_img = Column(String(25))
    user_intro = Column(String(160))
    user_iden = Column(Boolean, default=False)
    user_status = Column(Boolean, default=True)
