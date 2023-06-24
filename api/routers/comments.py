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
