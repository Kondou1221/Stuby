from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy import func, desc

import api.models.users as user_model
import api.models.posts as post_model
import api.models.comments as comment_model

#コメント作成
def create_comment(db: Session, comment_create: dict):
    try:
        new_comment = comment_model.Comment(**comment_create.dict())
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    except SQLAlchemyError as e:
        return False
    return new_comment

#コメント取得
def get_comment(db: Session, myuser_id:int, post_id: int):

    try:

        comment_good_count_table = db.query(
                                    func.count()
                                ).filter(
                                    comment_model.Comment.comment_id == comment_model.Commentgood.comment_id
                                ).group_by(comment_model.Commentgood.comment_id).label('comment_good_count')

        comment_status_table = db.query(
                                    func.count()
                                ).filter(
                                    comment_model.Commentgood.user_id == myuser_id,
                                    comment_model.Comment.comment_id == comment_model.Commentgood.comment_id
                                ).group_by(comment_model.Commentgood.comment_id).label('comment_status')
        
        comment_user = aliased(user_model.User)
        mention_user = aliased(user_model.User)

        comment = db.query(
            comment_model.Comment,
            comment_model.Comment.comment_id,
            comment_model.Comment.comment_sentence,
            comment_model.Comment.comment_img,
            comment_model.Comment.comment_create,
            comment_model.Comment.post_id,
            comment_user.user_id,
            comment_user.user_name,
            comment_user.icon_img,
            comment_user.user_gender,
            mention_user.user_id.label('mention_id'),
            mention_user.user_name.label('mention_user_name'),
            comment_good_count_table,
            comment_status_table
        ).join(
            comment_user,
            comment_user.user_id == comment_model.Comment.user_id
        ).join(
            mention_user,
            mention_user.user_id == comment_model.Comment.mention_id,
            isouter=True
        ).filter(
            comment_model.Comment.post_id == post_id
        ).order_by(desc(comment_model.Comment.comment_id)).all()
    
    except SQLAlchemyError as e:
        return False

    return comment

#リプライいいね追加
def insert_commentgood(db: Session, new_commentgood: dict):
    try:
        new_commentgood_data = comment_model.Commentgood(**new_commentgood.dict())
        db.add(new_commentgood_data)
        db.commit()
        db.refresh(new_commentgood_data)
    except SQLAlchemyError as e:
        return False
    
    return new_commentgood_data

#リプライいいね削除
def delete_commentgood(db: Session, delete_commentgood: dict):
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