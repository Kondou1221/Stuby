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
    user_old: int = None
    user_school_name: str = None
    user_faculty: str = None
    user_schoolyear: int = None
    fasubject: str = None
    wesubject: str = None
    icon_img: str = None
    pro_img: str = None
    user_intro: str = None

#結果のレスポンススキーマ
class result_response(BaseModel):
    message: str
    login_user_id: int

    class Config():
        orm_mode = True

#ユーザー取得レスポンススキーマ
class select_user(BaseModel):
    user_id: int
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
    icon_img: str = None
    pro_img: str = None
    user_intro: str = None
    user_iden: bool
    user_status: bool

    class Config():
        orm_mode = True
