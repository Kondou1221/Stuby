from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm.session import Session
from typing import List

import api.schemas.posts as post_schma
import api.cruds.posts as post_crud
from api.db import get_db

router = APIRouter(
    prefix='/post',
    tags=['posts']
)

#新規投稿
@router.post("/insert",
    summary="新規投稿",
    response_model=post_schma.create_post_response,
    status_code=status.HTTP_201_CREATED
    )
async def create_post(request: post_schma.create_post_request, db: Session = Depends(get_db)):
    new_post = post_crud.create_post(db, request)

    if not new_post:
        raise HTTPException(status_code=401, detail="create failed")

    return {"post_id" : new_post.post_id}

#投稿取得全てから20件
@router.get("/select/post",
    summary="投稿取得全てから20件",
    response_model=List[post_schma.select_post_id] or post_schma.select_post_id,
    status_code=status.HTTP_200_OK
    )
async def get_post(post_id: int = None, db: Session = Depends(get_db)):
    if post_id :
        post = post_crud.get_post_post_id(db, post_id)
    else:
        post = post_crud.get_post(db)

    if not post:
        raise HTTPException(status_code=404, detail="post does not found")

    return post

#投稿取得フォローしている人の投稿20件
@router.get("/select/post",
    summary="投稿取得フォローしている人の投稿20件",
    response_model=List[post_schma.select_post_id] or post_schma.select_post_id,
    status_code=status.HTTP_200_OK
    )
async def get_post(user_id: int, post_id: int = None, db: Session = Depends(get_db)):

    if user_id :
        if post_id:
            post = post_crud.get_post_user_id(db, user_id, post_id)
        else:
            post = post_crud.get_post_user_id(db, user_id)
    elif post_id:
        post = post_crud.get_post_post_id(db, post_id)
    else:
        post = post_crud.get_post(db)

    if not post:
        raise HTTPException(status_code=404, detail="post does not found")

    return post

#投稿のいいね追加
@router.post("/insert/postgood",
        summary="投稿のいいね追加",
        status_code=status.HTTP_204_NO_CONTENT
    )
async def insert_postgood(requst: post_schma.change_postgood, db :Session = Depends(get_db)):
    new_postgood = post_crud.insert_postgood(db, requst)

    if not new_postgood:
        raise HTTPException(status_code=401, detail="good failed")
    
    return

#投稿のいいね削除
@router.delete("/delete/postgood",
        summary="投稿のいいね削除",
        status_code=status.HTTP_204_NO_CONTENT
    )
async def delete_postgood(request: post_schma.change_postgood, db: Session = Depends(get_db)):
    delete_postgood_data = post_crud.delete_postgood_id(db, request)

    if not delete_postgood_data:
        raise HTTPException(status_code=401, detail="delete failed")
    
    return