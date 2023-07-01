from pydantic import BaseModel
import datetime

#ストーリー作成のリクエストスキーマ
class create_request(BaseModel):
    user_id: int
    story_sentence: str
    story_title: int

#ストーリーいいねする時と解除のリクエストスキーマ
class change_storygood(BaseModel):
    user_id: int
    story_good_id: int

#デフォルトのレスポンススキーマ
class default_response(BaseModel):
    pass

    class Config():
        orm_mode = True

#ストーリーを取得するレスポンススキーマ
class get_story(default_response):
    story_id: int
    user_id: int
    story_sentence: str
    story_title: str
    create_story: datetime.datetime