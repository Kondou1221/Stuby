from pydantic import BaseModel

#-----------------リクエスト-------------------------

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

#ログインのリクエストスキーマ
class cserlogin_request(BaseModel):
    user_email: str
    user_passwd: str

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
    user_status: bool = None

#-----------------レスポンス-------------------------

#デフォルトのレスポンススキーマ
class Defalut_responseModel(BaseModel):
    pass

    class Config():
        orm_mode = True

#ログイン結果のレスポンススキーマ
class result_response(Defalut_responseModel):
    login_user_id: int

#ユーザープロフィール詳細のレスポンススキーマ
class select_myprofile(Defalut_responseModel):
    user_id: int
    user_name: str
    user_gender: str
    user_old: int
    user_school_name: str
    user_faculty: str
    user_schoolyear: int
    fasubject: str
    wesubject: str
    icon_img: str = None
    pro_img: str = None
    user_intro: str = None
    user_status: bool
    follower_count: int
    user_postgood_count: int

#自分ではないユーザーのプロフィール詳細レスポンススキーマ
class select_other_userprofile(select_myprofile):
    follow_status: int #自分がフォローしているか

#マッチングの時のユーザー情報
class select_user_matcheing(Defalut_responseModel):
    user_id: int
    user_name: str
    user_gender: str
    user_old: int
    fasubject: str
    wesubject:str