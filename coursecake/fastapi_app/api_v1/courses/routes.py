# contains all routes for the courses endpoint
from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from ....database import crud, models
from ....database.sql import SessionLocal
from .. import schemas
router = APIRouter()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all", response_model=List[schemas.Course])
async def all_courses(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, offset = offset, limit = limit)
    return courses
