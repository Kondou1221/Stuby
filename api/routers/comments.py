from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm.session import Session
from typing import List

import api.schemas.comments as comment_schma
import api.cruds.comments as comment_crud
from api.db import get_db

router = APIRouter(
    prefix='/comment',
    tags=['comments']
)

#新規リプライ作成
@router.post("/insert",
    summary="新規リプライ作成",
    status_code=status.HTTP_204_NO_CONTENT
    )
async def create_comment(request: comment_schma.crate_commnet, db: Session = Depends(get_db) ):
    new_comment = comment_crud.create_comment(db, request)

    if not new_comment:
        raise HTTPException(status_code=401, detail="comment create failed")
    
    return

#リプライ取得
@router.get("/select/myuser_id/{myuser_id}/post_id/{post_id}",
    summary="リプライ取得",
    response_model=List[comment_schma.get_comment] or comment_schma.get_comment,
    status_code=status.HTTP_200_OK
    )
async def get_comment(myuser_id: int, post_id: int, db: Session = Depends(get_db) ):
    comment = comment_crud.get_comment(db, myuser_id, post_id)

    if not comment:
        raise HTTPException(status_code=404, detail="comment does not found")
    
    return comment

#リプライいいね追加
@router.post("/insert/good",
        summary="リプライいいね追加",
        status_code=status.HTTP_204_NO_CONTENT
    )
async def insert_commentgood(request: comment_schma.commentgood_request, db: Session = Depends(get_db) ):
    new_commentgood = comment_crud.insert_commentgood(db, request)

    if not new_commentgood:
        raise HTTPException(status_code=401, detail="good failed")
    
    return

#リプライいいね削除
@router.delete("/delete/good",
        summary="リプライいいね削除",
        status_code=status.HTTP_204_NO_CONTENT
    )
async def delete_commentgood(request: comment_schma.commentgood_request, db: Session = Depends(get_db) ):
    delete_commentgood = comment_crud.delete_commentgood(db, request)

    if not delete_commentgood:
        raise HTTPException(status_code=401, detail="delete failed")

    return
