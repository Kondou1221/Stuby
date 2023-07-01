from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

import api.models.users as user_model
import api.models.posts as post_model
import api.schemas.posts as post_schema

#投稿作成
def create_post(db: Session, post_create: post_schema.create_post_request):

    try:
        new_post = post_model.Post(**post_create.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except SQLAlchemyError as e:
        return False
    return new_post

#投稿20件取得
def get_post(db: Session):
    return db.query(
                post_model.Post,
                post_model.Post.post_id,
                post_model.Post.post_sentence,
                post_model.Post.post_img,
                post_model.Post.post_create,
                user_model.User.user_id,
                user_model.User.user_name,
                user_model.User.icon_img
            ).join(
                user_model.User,
                post_model.Post.user_id == user_model.User.user_id
            ).limit(25).all()

#投稿user_idありの場合 まだ
def get_post_user_id(db: Session, user_id: int, post_id: int = None):
    return db.query()

#投稿post_idありの場合 まだ
def get_post_post_id(db: Session, post_id: int):
    return db.query()

#投稿のいいね追加
def insert_postgood(db: Session, new_postgood: post_schema.change_postgood):
    new_postgood_data = post_model.Postgood(**new_postgood.dict())

    try:
        db.add(new_postgood_data)
        db.commit()
        db.refresh(new_postgood_data)
    except SQLAlchemyError as e:
        return False
    return new_postgood_data

#投稿のいいね削除
def delete_postgood_id(db: Session, delet_postgood: post_schema.change_postgood):
    delet_postgood = db.query(
        post_model.Postgood
        ).filter(
        post_model.Postgood.post_id == delet_postgood.post_id,
        post_model.Postgood.user_id == delet_postgood
        ).first()
    
    try:
        db.delete(delet_postgood)
        db.commit()
    except SQLAlchemyError as e:
        return False
    return delet_postgood

#投稿いいね取得 いらんかも
def get_post_count(db: Session, post_id: int):
    return db.query(post_model.Postgood).filter(post_model.Postgood.post_id == post_id).count()