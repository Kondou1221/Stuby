from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

import api.models.storys as story_model
import api.schemas.storys as story_schema

#ストーリー作成
def create_story(db: Session, story_create: story_schema.):

    try:
        new_story = story_model.Story(**story_create.dict())
        db.add(new_story)
        db.commit()
        db.refresh(new_story)
    except SQLAlchemyError as e:
        return False

    return new_story

#ストーリーいいね追加
def insert_storygood_id(db: Session, new_storygood_request: story_schema.):

    new_storygood = story_model.StoryGood(**new_storygood_request.dict())

    try:
        db.add(new_storygood)
        db.commit()
        db.refresh(new_storygood)
    except SQLAlchemyError as e:
        return False
    return new_storygood

#ストーリーいいね削除

#ストーリー表示