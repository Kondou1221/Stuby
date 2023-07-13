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

#ユーザーの新規登録
@router.post("/insert",
    summary="ユーザー新規登録",
    response_model=user_schma.result_response,
    status_code=status.HTTP_201_CREATED
    )
async def create_user(request: user_schma.crate_user_request, db: Session = Depends(get_db)):
    new_user = user_crud.create_user(db, request)

    if new_user == 0:
        raise HTTPException(status_code=400, detail="Email address already in use")
    
    if new_user == 1:
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

    if user == 0:
        raise HTTPException(status_code=404, detail=f"{request_user_login.user_email} not found")

    if user == 1:
        raise HTTPException(status_code=403, detail="Authentication failure")

    return {"login_user_id": user.user_id}

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

#マイプロフィール情報取得
@router.get("/select/profile/my_id/{user_id}",
    summary="ユーザープロフィール情報取得",
    response_model=user_schma.select_myprofile,
    status_code=status.HTTP_200_OK
    )
async def select_myprofile(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_myprofile(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user does not found")

    return user

#自分以外のユーザープロフィール情報取得
@router.get("/select/profile/my_id/{Myuser_id}/other_id/{other_user_id}",
    summary="自分以外のユーザープロフィール情報取得",
    response_model=user_schma.select_other_userprofile,
    status_code=status.HTTP_200_OK
    )
async def select_otherprofile(Myuser_id: int, other_user_id, db: Session = Depends(get_db)):
    user = user_crud.get_otherprofile(db, Myuser_id, other_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user does not found")

    return user

#マッチング(おすすめ順)
@router.get("/select/matching/recommendation",
    summary="マッチング(おすすめ順)",
    response_model=List[user_schma.select_user_matcheing] or user_schma.select_user_matcheing,
    status_code=status.HTTP_200_OK
    )
async def matching_recommendation(user_id: int = None, db: Session = Depends(get_db)):
    if user_id:
        user = user_crud.get_matching_user_recommendation(db, user_id)
    else:
        user = user_crud.get_matching_user_recommendation(db)

    if not user:
        raise HTTPException(status_code=404, detail="user does not found")
    
    return user

#マッチング(オンライン)
@router.get("/select/matching/online",
    summary="マッチング(オンライン)",
    response_model=List[user_schma.select_user_matcheing] or user_schma.select_user_matcheing,
    status_code=status.HTTP_200_OK
    )
async def matching_online(user_id: int = None, db: Session = Depends(get_db)):
    if user_id:
        user = user_crud.get_matching_user_online(db,user_id)
    else:
        user = user_crud.get_matching_user_online(db)
    if not user:
        raise HTTPException(status_code=404, detail="user does not found")

    return user

#マッチング(絞り込み)
@router.get("/select/matching/search",
    summary="マッチング(絞り込み)",
    response_model=List[user_schma.select_user_matcheing] or user_schma.select_user_matcheing,
    status_code=status.HTTP_200_OK
    )
async def matching_search(user_id: int = None, fasubject: str = None, wesubject: str = None, user_old: int = None, user_gender: str = None, db: Session = Depends(get_db)):
    search_list = dict()

    if user_id:
        search_list["user_id"] = user_id
    if fasubject:
        search_list["fasubject"] = fasubject
    if wesubject:
        search_list["wesubject"] = wesubject
    if user_old:
        search_list["user_old"] = user_old
    if user_gender:
        search_list["user_gender"] = user_gender
    
    user = user_crud.get_matching_user_search(db, search_list)
    if not user:
        raise HTTPException(status_code=404, detail="user does not found")

    return user