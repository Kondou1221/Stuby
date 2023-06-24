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

#投稿取得20件
@router.get("/select/post",
    summary="投稿取得20件",
    response_model=List[post_schma.select_post] or post_schma.select_post,
    status_code=status.HTTP_200_OK
    )
async def get_post(post_id: int = None, db: Session = Depends(get_db)):
    if post_id :
        post = post_crud.get_post(db, post_id)
    else:
        post = post_crud.get_post(db)

    if not post:
        raise HTTPException(status_code=404, detail="post does not exist")

    return post

#投稿のいいね数取得
@router.get("/select/count/{post_id}",
    summary="投稿のいいね数取得",
    status_code=status.HTTP_200_OK
    )
async def get_post_id(post_id: int, db: Session = Depends(get_db)):
    return {"post_count":post_crud.get_post_count(db, post_id)}

#新規投稿
@router.post("/insert",
    summary="新規投稿",
    status_code=status.HTTP_201_CREATED
    )
async def create_post(request: post_schma.create_post_request, db: Session = Depends(get_db)):
    new_post = post_crud.create_post(db, request)

    if not new_post:
        raise HTTPException(status_code=500, detail="Signup failed")

    return {"message":"status OK"}

#投稿のいいね追加
# @router.post("/insert/good",
#     summary="",
#     status_code=status.HTTP_201_CREATED
#     )
# async def 