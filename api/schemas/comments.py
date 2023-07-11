from pydantic import BaseModel
import datetime

#----------------リクエストスキーマ--------------------

#コメント作成のリクエストスキーマ
class crate_commnet(BaseModel):
    user_id: int
    post_id: int
    comment_sentence: str = None
    comment_img: str = None
    mention_id: int = None

#いいねの追加と削除のリクエストスキーマ
class commentgood_request(BaseModel):
    comment_id: int
    user_id: int

#----------------レスポンススキーマ--------------------

#デフォルトのレスポンススキーマ
class default_response(BaseModel):
    pass

    class Config():
        orm_mode = True

class get_comment(default_response):
    comment_id: int
    comment_sentence: str = None
    comment_img: str = None
    comment_create: datetime.datetime
    post_id: int
    user_id: int
    user_name: str
    icon_img: str = None
    user_gender:str
    mention_id: int = None
    mention_user_name: str = None
    comment_good_count: int = None
    comment_status: int = None
