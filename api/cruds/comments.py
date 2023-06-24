from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

import api.models.users as user_model
import api.models.posts as post_model
import api.models.comments as comment_model

import api.schemas.comments as comment_schma

def create_comment(db: Session, comment_create: comment_schma.base_comment_schma):
    try:
        new_comment = comment_model.Comment(**comment_create.dict())
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    except SQLAlchemyError as e:
        return False
    return new_comment

def get_comment(db: Session, post_id: int):
    comment = db.query(
        comment_model.Comment,
        comment_model.Comment.comment_id,
        comment_model.Comment.comment_sentence,
        comment_model.Comment.comment_create,
        comment_model.Comment.post_id,
        user_model.User.user_id,
        user_model.User.user_name
    ).join(
        user_model.User,
        comment_model.Comment.user_id == user_model.User.user_id
    ).filter(
        comment_model.Comment.post_id == post_id
    ).all()

    return comment

def insert_commentgood(db: Session, new_commentgood: comment_schma.commentgood_request):
    try:
        new_commentgood_data = comment_model.Commentgood(**new_commentgood.dict())
        db.add(new_commentgood_data)
        db.commit()
        db.refresh(new_commentgood_data)
    except SQLAlchemyError as e:
        return False
    
    return new_commentgood_data

def delete_commentgood(db: Session, delete_commentgood: comment_schma.commentgood_request):
    try:

        delete_commentgood_data = db.query(
                comment_model.Commentgood
            ).filter(
                comment_model.Commentgood.comment_id == delete_commentgood.comment_id,
                comment_model.Commentgood.user_id == delete_commentgood.user_id
            ).first()
        
        db.delete(delete_commentgood_data)
        db.commit()
        db.refresh(delete_commentgood_data)
    except SQLAlchemyError as e:
        return False
    
    return delete_commentgood_data