from sqlalchemy import or_
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased

import api.models.follows as follow_model
import api.models.users as user_model
import api.schemas.follows as follow_schma

#フォロー追加
def insert_follow(db: Session, new_follow: follow_schma.change_follow):

    if not db.query(user_model.User).filter(or_(user_model.User.user_id == new_follow.follow_id, user_model.User.user_id == new_follow.follower_id)).first():
        return 0
    
    new_follow_data = follow_model.Follow(**new_follow.dict())
    try:
        db.add(new_follow_data)
        db.commit()
        db.refresh(new_follow_data)
    except SQLAlchemyError as e:
        return 1
    return new_follow_data

#フォロー削除
def delete_follow_id(db:Session, delete_follow: follow_schma.change_follow):    

    delete_follow_data =  db.query(follow_model.Follow).filter(follow_model.Follow.follow_id == delete_follow.follow_id, follow_model.Follow.follower_id == delete_follow.follower_id).first()
    
    if not delete_follow_data:
        return 1
    try:
        db.delete(delete_follow_data)
        db.commit()
    except SQLAlchemyError as e:
        return 2
    return delete_follow_data