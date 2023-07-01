from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm.session import Session
from typing import List

import api.schemas.users as user_schma
import api.cruds.users as user_crud
from api.db import get_db

router = APIRouter(
    prefix='/user',
    tags=['users']
)

#ユーザー新規登録
@router.post("/insert",
    summary="ユーザー新規登録",
    response_model=user_schma.result_response,
    status_code=status.HTTP_201_CREATED
    )
async def create_user(request: user_schma.crate_user_request, db: Session = Depends(get_db)):
    new_user = user_crud.create_user(db, request)

    if new_user == 1:
        raise HTTPException(status_code=400, detail="Email address already in use")
    
    if new_user == 2:
        raise HTTPException(status_code=401, detail="Signup failed")

    return {"login_user_id": new_user.user_id}

#ユーザーログイン
@router.post("/login",
    summary="ユーザーログイン",
    response_model=user_schma.result_response,
    status_code=status.HTTP_200_OK
    )
async def login_user(request_user_login: user_schma.cserlogin_request, db: Session = Depends(get_db)):
    user = user_crud.login_user(db, request_user_login)

    if user == 1:
        raise HTTPException(status_code=404, detail=f"{request_user_login.user_email} not found")

    if user == 2:
        raise HTTPException(status_code=401, detail="Authentication failure")

    return {"login_user_id": user.user_id}

#ユーザーマイプロフィール情報取得
@router.get("/select/profile/my_id/{user_id}",
    summary="ユーザープロフィール情報取得",
    response_model=user_schma.select_userprofile,
    status_code=status.HTTP_200_OK
    )
async def select_myprofile(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_myprofile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user does not found")

    return user

#自分以外のユーザープロフィール情報取得
@router.get("/select/profile/my_id/{Myuser_id}/other_id/{Oh_id}",
    summary="自分以外のユーザープロフィール情報取得",
    response_model=user_schma.get_user_otherprofile,
    status_code=status.HTTP_200_OK
    )
async def select_otherprofile(user_id: int, Oh_id, db: Session = Depends(get_db)):
    user = user_crud.get_otherprofile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user does not found")

    return user

#ユーザー情報変更
@router.put("/update",
    summary="ユーザー情報変更",
    status_code=status.HTTP_204_NO_CONTENT
    )
async def update_user(request_change_user: user_schma.update_user_request, db: Session = Depends(get_db)):
    user = user_crud.update_user(db, request_change_user)

    if user == 0:
        raise HTTPException(status_code=404, detail="user does not found")
    
    if user == 1:
        raise HTTPException(status_code=400, detail="user update failed")

    return