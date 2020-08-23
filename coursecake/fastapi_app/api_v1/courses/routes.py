# contains all routes for the courses endpoint
from typing import List, Optional

from fastapi import Depends, APIRouter, BackgroundTasks, Query
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



@router.get("/search/{university}", response_model=List[schemas.Course])
async def search_courses(
    university: str = Query(
        "uci",
        title = "university code",
        description = "university code is the domain name for your university. Ex: <university>.edu"
    ),
    term_id: Optional[str] = Query(
        "2020-fall",
        title = "Term Code",
        description = "Search for courses in this term; YEAR-SEASON. Ex: Spring Semester = 2021-spring"
    ),
    offset: Optional[int] = Query(
        0,
        description = "Use this to see next page of results"
    ),
    limit: Optional[int] = Query(
        500,
        description = "Higher limits can create slower responses"
    ),
    db: Session = Depends(get_db)

):
    courses = crud.CourseQuery(db, university, term_id=term_id, offset=offset, limit=limit).search()
    return courses
