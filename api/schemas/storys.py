from pydantic import BaseModel
import datetime

#-----------------リクエスト-------------------------

#ストーリー作成のリクエストスキーマ
class create_story(BaseModel):
    user_id: int
    story_sentence: str
    story_title: str

#ストーリーいいねする時と解除のリクエストスキーマ
class change_storygood(BaseModel):
    story_id: int
    user_id: int

#-----------------レスポンス-------------------------

#デフォルトのレスポンススキーマ
class default_response(BaseModel):
    pass

    class Config():
        orm_mode = True

#ストーリーを取得するレスポンススキーマ
class get_story(default_response):
    user_id: int
    user_name: str
    user_icon: str = None
    story_id: int
    story_sentence: str
    story_title: str
    create_story: datetime.datetime
    story_good_count: int = None
    story_good_status: int = None

#ホーム画面でのストーリー取得
class get_home_story(default_response):
    story_id: int
    user_id: int
    user_name: str
    user_icon: str = None
