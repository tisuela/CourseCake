# contains all routes for the courses endpoint
from typing import List

from fastapi import Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session

from ....database import crud, models, sql
from .. import schemas
router = APIRouter()

# dependency
def get_db():
    db = sql.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all", response_model=List[schemas.Course])
async def all_courses(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, offset = offset, limit = limit)
    return courses



@router.get("/search/{university}")
async def search_courses(university: str):
    return []
