from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from sqlalchemy import and_

import api.models.users as user_model
import api.models.follows as follow_model
import api.models.posts as post_model

#ユーザー新規登録
def create_user(db: Session, user_create: dict):#dictに変えた
    existing_user = db.query(user_model.User).filter(user_model.User.user_email == user_create.user_email).first()

    if existing_user :
        return 0
    
    # user_create.user_passwd = Hash.get_password_hash(user_create.user_passwd)

    try:
        new_user = user_model.User(**user_create.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as e:
        return 1
    return new_user

#ユーザーログイン
def login_user(db: Session, user_login: dict):#dictに変えた
    
    try:
        user = db.query(user_model.User, user_model.User.user_id, user_model.User.user_email, user_model.User.user_passwd).filter(user_model.User.user_email == user_login.user_email).one()
    except SQLAlchemyError as e:
        return 0

    # if not Hash.verify_password(user.user_passwd, user_login.user_passwd) :
    #     return 2

    if not user.user_passwd == user_login.user_passwd:
        return 1


    return user

#ユーザー情報変更
def update_user(db: Session, change_user: dict):#dictに変えた
    user = db.query(user_model.User).get(change_user.user_id)

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
    if not change_user.user_status is None:
        user.user_status = change_user.user_status

    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except SQLAlchemyError as e:
        return 1

    return user

#ユーザーマイプロフィール取得
def get_myprofile(db: Session, user_id: int):

    try:
        follow_count_table = aliased(
                db.query(
                    func.count().label('follower_count')
                ).filter(
                    follow_model.Follow.follower_id == user_id
                ).subquery(),
                name="follow_count_table"
            )

        user_postgood_count = aliased(
                db.query(
                    post_model.Post.user_id,
                    func.count().label('user_postgood_count')
                    ).join(post_model.Postgood,
                        post_model.Post.post_id == post_model.Postgood.post_id
                    ).filter(
                        post_model.Post.user_id == user_id
                    ).subquery(),
                    name="user_postgood_count"
            )

        user = db.query(
                user_model.User.user_id,
                user_model.User.user_name,
                user_model.User.user_gender,
                user_model.User.user_old,
                user_model.User.user_school_name,
                user_model.User.user_faculty,
                user_model.User.user_schoolyear,
                user_model.User.fasubject,
                user_model.User.wesubject,
                user_model.User.icon_img,
                user_model.User.pro_img,
                user_model.User.user_intro,
                user_model.User.user_status,
                user_postgood_count.c.user_postgood_count,
                follow_count_table.c.follower_count
            ).filter(
                user_model.User.user_id == user_id
            ).one()
    except SQLAlchemyError as e:
        return False

    return user

#ユーザー他の人のプロフィール取得 まだ
def get_otherprofile(db: Session, myuser_id: int, other_user_id: int):
    follow_count_table = aliased(
            db.query(
                func.count().label('follower_count')
            ).filter(
                follow_model.Follow.follower_id == other_user_id
            ).subquery(),
            name="follow_count_table"
        )

    user_postgood_count = aliased(
            db.query(
                post_model.Post.user_id,
                func.count().label('user_postgood_count')
                ).join(post_model.Postgood,
                    post_model.Post.post_id == post_model.Postgood.post_id
                ).filter(
                    post_model.Post.user_id == other_user_id
                ).subquery(),
                name="user_postgood_count"
        )
    
    follow_status_table = aliased(
            db.query(
                    func.count().label('follow_status')
                ).filter(
                    follow_model.Follow.follow_id == myuser_id, follow_model.Follow.follower_id == other_user_id
                ).subquery(),
                name="follow_status_table"
                )

    user = db.query(
            user_model.User.user_id,
            user_model.User.user_name,
            user_model.User.user_gender,
            user_model.User.user_old,
            user_model.User.user_school_name,
            user_model.User.user_faculty,
            user_model.User.user_schoolyear,
            user_model.User.fasubject,
            user_model.User.wesubject,
            user_model.User.icon_img,
            user_model.User.pro_img,
            user_model.User.user_intro,
            user_model.User.user_status,
            follow_count_table.c.follower_count,
            user_postgood_count.c.user_postgood_count,
            follow_status_table.c.follow_status
        ).filter(
            user_model.User.user_id == other_user_id
        ).one()
    
    print(user)
    
    return user

#マッチング(おすすめ順)
def get_matching_user_recommendation(db: Session, user_id: int = None):

    if user_id:

        user = db.query(
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    user_model.User.fasubject,
                    user_model.User.wesubject
                ).filter(
                    user_model.User.user_id > user_id,
                ).order_by(
                    user_model.User.user_id
                ).limit(20).all()
    
    else:
        user = db.query(
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    user_model.User.fasubject,
                    user_model.User.wesubject
                ).order_by(
                    user_model.User.user_id
                ).limit(20).all()
        
    return user

#マッチング(オンライン)
def get_matching_user_online(db: Session, user_id: int = None):

    if user_id:

        user = db.query(
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    user_model.User.fasubject,
                    user_model.User.wesubject
                ).filter(
                    user_model.User.user_id > user_id,
                    user_model.User.user_status == True
                ).order_by(
                    user_model.User.user_id
                ).limit(20).all()

    else:
        user = db.query(
                    user_model.User.user_id,
                    user_model.User.user_name,
                    user_model.User.user_gender,
                    user_model.User.user_old,
                    user_model.User.fasubject,
                    user_model.User.wesubject
                ).filter(
                    user_model.User.user_status == True
                ).order_by(
                    user_model.User.user_id
                ).limit(20).all()
        
    return user

#マッチング(絞り込み)
def get_matching_user_search(db: Session, search_list: dict):
    filters = []

    try:
        if "user_id" in search_list.keys():
            filters.append(user_model.User.user_id == search_list["user_id"])
        if "fasubject" in search_list.keys():
            filters.append(user_model.User.fasubject == search_list["fasubject"])
        if "wesubject" in search_list.keys():
            filters.append(user_model.User.wesubject == search_list["wesubject"])
        if "user_old" in search_list.keys():
            filters.append(user_model.User.user_old == search_list["user_old"])
        if "user_gender" in search_list.keys():
            filters.append(user_model.User.user_gender == search_list["user_gender"])

        user = db.query(
                user_model.User.user_id,
                user_model.User.user_name,
                user_model.User.user_gender,
                user_model.User.user_old,
                user_model.User.fasubject,
                user_model.User.wesubject
            ).filter(
                and_(*filters)
            ).order_by(
                user_model.User.user_id
            ).limit(20).all()
        
    except SQLAlchemyError as e:
        return e.args

    return user