from sqlalchemy.orm.session import Session

import api.models.follows as follow_model
import api.models.users as user_model
import api.schemas.follows as follow_schma

#
def select_follow(db: Session):
    return db.query(follow_model.Follow).all()

def get_follower_count(db: Session, follower_id: int):
    return db.query(follow_model.Follow).filter(follow_model.Follow.follower_id == follower_id).count()

def get_followed_count(db: Session, followed_id: int):
    return db.query(follow_model.Follow).filter(follow_model.Follow.followed_id == followed_id).count()

def insert_follow(db: Session, new_follow: follow_schma.select_follow):

    if not db.query(user_model.User).filter(user_model.User.user_id == new_follow.follower_id).first():
        return 0
    elif not db.query(user_model.User).filter(user_model.User.user_id == new_follow.followed_id).first():
        return 0

    new_follow_data = follow_model.Follow(**new_follow.dict())
    db.add(new_follow_data)
    db.commit()
    db.refresh(new_follow_data)

    return new_follow_data

def delete_follow_id(db:Session, delete_follow: follow_schma.select_follow):
    if not db.query(user_model.User).filter(user_model.User.user_id == delete_follow.follower_id).first():
        return 0
    elif not db.query(user_model.User).filter(user_model.User.user_id == delete_follow.followed_id).first():
        return 0

    delete_follow_data =  db.query(follow_model.Follow).filter(follow_model.Follow.follower_id == delete_follow.follower_id, follow_model.Follow.followed_id == delete_follow.followed_id).first()
    if not delete_follow_data:
        return False
    db.delete(delete_follow_data)
    db.commit()
    return delete_follow_data