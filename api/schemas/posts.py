from pydantic import BaseModel
import datetime

#新規の投稿のリクエストスキーマ
class create_post_request(BaseModel):
    user_id: int
    post_sentence: str = None
    post_img: str = None

#投稿のいいねする時と解除する時のリクエストスキーマ
class change_postgood(BaseModel):
    post_id: int
    user_id: int

#デフォルトのレスポンススキーマ
class default_response(BaseModel):
    pass

    class Config():
        orm_mode = True

#新規投稿レスポンススキーマ
class create_post_response(default_response):
    post_id: int

#投稿ユーザー情報取得20件
class select_post_id(default_response):
    post_id: int
    user_id: int
    post_sentence: str = None
    post_img: str = None
    post_create: datetime.datetime
    user_name: str
    icon_img: str
    user_gender: str
    user_old: int
    post_good_count: int
    post_comment_count: int