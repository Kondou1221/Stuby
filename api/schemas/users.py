from pydantic import BaseModel

#ログインのリクエストスキーマ
class cserlogin_request(BaseModel):
    user_email: str
    user_passwd: str

#新規登録のリクエストスキーマ
class crate_user_request(BaseModel):
    user_name: str
    user_email: str
    user_passwd: str
    user_gender: str
    user_old: int
    user_school_name: str
    user_faculty: str
    user_schoolyear: int
    fasubject: str
    wesubject:str

#変更のリクエストスキーマ
class update_user_request(BaseModel):
    user_id: int
    user_name: str = None
    user_email: str = None
    user_passwd: str = None
    user_gender: str = None
    user_school_name: str = None
    user_faculty: str = None
    user_schoolyear: int = None
    fasubject: str = None
    wesubject: str = None
    icon_img: str = None
    pro_img: str = None
    user_intro: str = None

#デフォルトのレスポンススキーマ
class ResponseModel(BaseModel):
    pass

    class Config():
        orm_mode = True

#ログイン結果のレスポンススキーマ
class result_response(ResponseModel):
    login_user_id: int

#ユーザープロフィール詳細のレスポンススキーマ
class select_userprofile(ResponseModel):
    user_id: int
    user_name: str
    user_gender: str
    user_old: int
    user_school_name: str
    user_faculty: str
    user_schoolyear: int
    fasubject: str
    wesubject:str
    icon_img: str = None
    pro_img: str = None
    user_intro: str = None
    user_status: bool
    follower_count: int #フォローされている数
    user_postgood_count: int #投稿のいいねの数

#自分ではないユーザーのプロフィール詳細レスポンススキーマ
class get_user_otherprofile(select_userprofile):
    follow_status: bool #自分がフォローしているか

class get_user_matcheing(ResponseModel):
    user_id: int
    user_name: str
    user_old: int
    fasubject: str
    wesubject:str