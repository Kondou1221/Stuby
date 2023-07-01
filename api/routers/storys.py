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
