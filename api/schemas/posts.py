from pydantic import BaseModel
import datetime

#新規の投稿のリクエストスキーマ
class create_post_request(BaseModel):
    user_id: int
    post_sentence: str = None
    post_img: str = None

#投稿情報のレスポンススキーマ
class select_post(BaseModel):
    post_id: int
    post_sentence: str = None
    post_img: str = None
    post_create: datetime.datetime
    user_id: int
    user_name: str
    user_icon: str = None

    class Config():
        orm_mode = True