from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

import api.models.storys as story_model
import api.models.users as user_model

#ストーリー作成
def create_story(db: Session, story_create: dict):

    try:
        new_story = story_model.Story(**story_create.dict())
        db.add(new_story)
        db.commit()
        db.refresh(new_story)
    except SQLAlchemyError as e:
        return False

    return new_story

#ストーリー表示 まだ
def select_story(db: Session, story_id: int):
    return

#ホーム画面でのストーリー表示(他人)
def select_home_story(db: Session):
    return db.query(
                story_model.Story,
                story_model.Story.story_id,
                user_model.User.user_id,
                user_model.User.user_name,
                user_model.User.icon_img
            ).join(
                user_model.User,
                user_model.User.user_id == story_model.Story.user_id
            ).all()

#ストーリーいいね追加
def insert_storygood_id(db: Session, new_storygood_request: dict):

    new_storygood = story_model.StoryGood(**new_storygood_request.dict())

    try:
        db.add(new_storygood)
        db.commit()
        db.refresh(new_storygood)
    except SQLAlchemyError as e:
        return False
    return new_storygood

#ストーリーいいね削除
def delete_storygood_id(db: Session, delete_storygood: dict):
    delete_storygood_data = db.query(
            story_model.StoryGood
        ).filter(
            story_model.StoryGood.story_id == delete_storygood.story_id,
            story_model.StoryGood.user_id == delete_storygood.user_id
        ).first()
    
    try:
        db.delete(delete_storygood_data)
        db.commit()
    except SQLAlchemyError as e:
        return False
    
    return delete_storygood_data