from pydantic import BaseModel

#フォローする時と解除する時のスキーマ
class change_follow(BaseModel):
    follower_id: int #フォローするuser_id
    followed_id: int #フォローされるuser_id

#デフォルトのレスポンススキーマ
class default_response(BaseModel):
    pass

    class Config():
        orm_mode = True