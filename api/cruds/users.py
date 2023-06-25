from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

import api.models.users as user_model
import api.schemas.users as user_schema

#ユーザー新規登録
def create_user(db: Session, user_create: user_schema.crate_user_request):
    existing_user = db.query(user_model.User).filter(user_model.User.user_email == user_create.user_email).first()

    if existing_user :
        return 1
    
    try:
        new_user = user_model.User(**user_create.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as e:
        return 2
    return new_user

#ユーザー全取得
def get_user_all(db: Session):
    users = db.query(user_model.User).all()

    return users

#ユーザープロフィール取得
def get_userprofile(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.user_id == user_id).first()

#ユーザーいいね取得
def get_usergood_count(db: Session, user_id: int):
    return db.query(user_model.Usergood).filter(user_model.Usergood.liked_user_id == user_id).count()

#ユーザーログイン
def login_user(db: Session, user_login: user_schema.cserlogin_request):
    user = db.query(user_model.User).filter(user_model.User.user_email == user_login.user_email).first()
    if user and user.user_passwd == user_login.user_passwd:
        return user

    return False

#ユーザー情報変更
def update_user(db: Session, change_user:user_schema.update_user_request):
    user = db.query(user_model.User).filter(user_model.User.user_id == change_user.user_id).first()

    if not user:
        return 0

    if not change_user.user_name is None:
        user.user_name = change_user.user_name
    if not change_user.user_email is None:
        user.user_email = change_user.user_email
    if not change_user.user_passwd is None:
        user.user_passwd = change_user.user_passwd
    if not change_user.user_gender is None:
        user.user_gender = change_user.user_gender
    if not change_user.user_old is None:
        user.user_old = change_user.user_old
    if not change_user.user_school_name is None:
        user.user_school_name = change_user.user_school_name
    if not change_user.user_faculty is None:
        user.user_faculty = change_user.user_faculty
    if not change_user.user_schoolyear is None:
        user.user_schoolyear = change_user.user_schoolyear
    if not change_user.fasubject is None:
        user.fasubject = change_user.fasubject
    if not change_user.wesubject is None:
        user.wesubject = change_user.wesubject
    if not change_user.icon_img is None:
        user.icon_img = change_user.icon_img
    if not change_user.pro_img is None:
        user.pro_img = change_user.pro_img
    if not change_user.user_intro is None:
        user.user_intro = change_user.user_intro
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
