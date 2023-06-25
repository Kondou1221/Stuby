from pydantic import BaseModel

#結果のレスポンススキーマ
class result_response(BaseModel):
    message: str

    class Config():
        orm_mode = True

#フォロー全取得レスポンススキーマ
class select_follow(BaseModel):
    follower_id: int
    followed_id: int

    class Config():
        orm_mode = True

#フォローしている数のレスポンススキーマ
# class follower_select_id(BaseModel):
#     followed_count: int

#     class Config():
#         orm_mode = True

#フォローされている数のレスポンススキーマ
# class followed_select_id(BaseModel):
#     follower_count: int

#     class Config():
#         orm_mode = True
