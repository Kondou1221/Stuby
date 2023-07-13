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

#フォロー追加
@router.post("/insert",
    summary="フォロー追加",
    status_code=status.HTTP_204_NO_CONTENT
    )
async def insert_follower_id(request: follow_schma.change_follow, db: Session = Depends(get_db)):
    new_follow = follow_crud.insert_follow(db, request)

    if new_follow == 0:
        raise HTTPException(status_code=401, detail="already followed")

    elif new_follow == 1:
        raise HTTPException(status_code=401, detail="follow failed")

    return 

#フォロー削除
@router.delete("/delete",
    summary="フォロー削除",
    status_code=status.HTTP_204_NO_CONTENT
    )
async def delete_follower_id(request: follow_schma.change_follow, db: Session = Depends(get_db)):
    delete_follow = follow_crud.delete_follow_id(db, request)
    
    if delete_follow == 2:
        raise HTTPException(status_code=404, detail="not followed")

    elif delete_follow == 2:
        raise HTTPException(status_code=401, detail="follow failed")

    return

