from sqlalchemy.orm.session import Session
import datetime

import api.models.users as user_model
import api.models.posts as post_model
import api.schemas.posts as post_schema

def create_post(db: Session, post_create: post_schema.create_post_request):
    new_post = post_model.Post(**post_create.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_post(db: Session, post_create_data: datetime.datetime = None):
    if post_create_data:
        post = db.query(post_model.Post,
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
            ).filter(post_model.Post.post_create > post_create_data).limit(25).all()
    else:
        post = db.query(post_model.Post,
                post_model.Post.post_id,
                post_model.Post.post_sentence,
                post_model.Post.post_img,
                post_model.Post.post_create,
                user_model.User.user_id,
                user_model.User.user_name,
                user_model.User.icon_img
                ).join(user_model.User, post_model.Post.user_id == user_model.User.user_id).limit(25).all()
    return post

def get_post_count(db: Session, post_id: int):
    return db.query(post_model.Postgood).filter(post_model.Postgood.post_id == post_id).count()