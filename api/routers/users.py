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
        raise HTTPException(status_code=400, detail="Already Registered")
    
    if new_user == 2:
        raise HTTPException(status_code=401, detail="Signup failed")

    return {"message":"status OK", "login_user_id": new_user.user_id}

# ユーザー全取得
@router.get("/select/all",
    summary="ユーザー全取得",
    response_model=List[user_schma.select_user] or user_schma.select_user,
    status_code=status.HTTP_200_OK
    )
async def get_user_all(db: Session = Depends(get_db)):
    user = user_crud.get_user(db)

    if not user:
        raise HTTPException(status_code=404, detail="user does not exist")

    return user

#ユーザー情報取得idで絞り込み
@router.get("/select/id/{user_id}",
    summary="ユーザー情報取得idで絞り込み",
    response_model=user_schma.select_user,
    status_code=status.HTTP_200_OK
    )
async def select_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="user does not exist")

    return user

#ユーザーログイン
@router.post("/login",
    summary="ユーザーログイン",
    response_model=user_schma.result_response,
    status_code=status.HTTP_200_OK
    )
async def login_user(request_user_login: user_schma.cserlogin_request, db: Session = Depends(get_db)):
    user = user_crud.login_user(db, request_user_login)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email address or password")

    return {"message":"status OK", "login_user_id": user.user_id}

#ユーザー情報変更
@router.put("/update",
    summary="ユーザー情報変更",
    response_model=user_schma.result_response
    )
async def update_user(request_change_user: user_schma.update_user_request, db: Session = Depends(get_db)):
    user = user_crud.update_user(db, request_change_user)

    if user == 0:
        raise HTTPException(status_code=404, detail="user does not exist")

    return {"message":"status OK", "login_user_id": user.user_id}