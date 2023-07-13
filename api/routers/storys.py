from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm.session import Session
from typing import List

import api.schemas.storys as story_schma
import api.cruds.storys as story_crud
from api.db import get_db

router = APIRouter(
    prefix='/story',
    tags=['story']
)

#ストーリー作成
@router.post("/insert",
    summary="ストーリー作成",
    status_code=status.HTTP_201_CREATED
)
def crate_story(create_story: story_schma.create_story, db: Session = Depends(get_db)):
    story = story_crud.create_story(db, create_story)

    if not story:
        raise HTTPException(status_code=401, detail="create failed")
    
    return 

#ストーリー表示 決めてる最中
@router.get("/select/story_id/{story_id}",
    summary="ストーリー表示",
    response_model=story_schma.get_story,
    status_code=status.HTTP_200_OK
)
def get_story(story_id: int, db: Session = Depends(get_db)):
    return

#ホーム画面でのストーリー表示(他人)
@router.get("/select/home",
    summary="ホーム画面でのストーリー表示(他人)",
    response_model=list[story_schma.get_home_story] or story_schma.get_home_story,
    status_code=status.HTTP_200_OK
)
def get_home_oterstory(db: Session = Depends(get_db)):
    story = story_crud.select_home_story(db)

    if not story:
        raise HTTPException(status_code=404, detail="story not found")

    return story

#ストーリーにいいねする時
@router.post("/insert/storygood",
    summary="ストーリーにいいねする時",
    status_code=status.HTTP_201_CREATED
)
def insert_storygood(request: story_schma.change_storygood, db: Session = Depends(get_db)):
    new_storygood = story_crud.insert_storygood_id(db, request)

    if not new_storygood:
        raise HTTPException(status_code=401, detail="good failed")
    
    return

#ストーリーのいいね解除する時
@router.delete("/delete/storygood",
    summary="ストーリーのいいね解除する時",
    status_code=status.HTTP_201_CREATED
)
def insert_storygood(request: story_schma.change_storygood, db: Session = Depends(get_db)):
    new_storygood = story_crud.delete_storygood_id(db, request)

    if not new_storygood:
        raise HTTPException(status_code=401, detail="good failed")
    
    return

