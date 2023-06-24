from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm.session import Session
from typing import List

import api.schemas.follows as follow_schma
import api.cruds.follows as follow_crud
from api.db import get_db

router = APIRouter(
    prefix='/follow',
    tags=['follows']
)

# フォロー表全取得
@router.get("/select/all",
    summary="フォロー表全取得",
    response_model=List[follow_schma.select_follow] or follow_schma.select_follow
    )
async def get_follow_all(db: Session = Depends(get_db)):
    follow = follow_crud.select_follow(db)

    if not follow:
        raise HTTPException(status_code=404, detail="follow does not exist")

    return follow

# フォローしている数取得
@router.get("/follower/count/{id}",
    summary="フォローしている数取得",
    response_model=follow_schma.follower_select_id
    )
async def get_follower_count(id: int, db: Session = Depends(get_db)):
    return {"followed_count":follow_crud.get_follower_count(db, id)}

# フォローされている数取得
@router.get("/followed/count/{id}",
    summary="フォローされている数取得",
    response_model=follow_schma.followed_select_id
    )
async def get_followed_count(id: int, db: Session = Depends(get_db)):
    return {"follower_count":follow_crud.get_followed_count(db, id)}

#フォロー追加
@router.post("/insert",
    summary="フォロー追加",
    response_model=follow_schma.result_response
    )
async def insert_follower_id(request: follow_schma.select_follow, db: Session = Depends(get_db)):
    new_follow = follow_crud.insert_follow(db, request)
    if new_follow == 0:
        raise HTTPException(status_code=404, detail="user does not exist")

    return {"message":"status OK"}

#フォロー削除
@router.delete("/delete",
    summary="フォロー削除",
    response_model=follow_schma.result_response
    )
async def delete_follower_id(request: follow_schma.select_follow, db: Session = Depends(get_db)):
    delete_follow = follow_crud.delete_follow_id(db, request)

    if delete_follow == 0:
        raise HTTPException(status_code=404, detail="user does not exist")
    elif not delete_follow:
        raise HTTPException(status_code=401, detail="not following")

    return {"message":"status OK"}

