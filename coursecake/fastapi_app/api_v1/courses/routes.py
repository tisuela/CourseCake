# contains all routes for the courses endpoint
from typing import List, Optional

from fastapi import Depends, APIRouter, BackgroundTasks, Query, Request
from sqlalchemy.orm import Session

from ....database import crud, models, sql
from .. import schemas
from . import utils

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
    request: Request,
    university: str,
    term_id: Optional[str] = Query(
        "2020-fall",
        title = "Term Code",
        description = "Search for courses in this term; YEAR-SEASON. Ex: Spring Semester = 2021-spring"
    ),
    code: Optional[str] = Query(
        None,
        title = "Course code",
        description = "Unique within the term of a University"
    ),
    name: Optional[str] = Query(
        None,
        title = "Course name",
        description = "The formal name of a course. Ex: course 101"
    ),
    title: Optional[str] = Query(
        None,
        title = "Course title",
        description = "A more readable name of a course. Ex: Intro to course"
    ),
    department: Optional[str] = Query(
        None,
        title = "Department code",
        description = "See your university's website for the code. Ex: COMPSCI"
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
    courses = crud.CourseQuery(db, university, request.query_params, term_id=term_id, offset=offset, limit=limit).search()
    return courses



@router.get("/live-search/{university}")
async def search_courses(
    request: Request,
    university: str,
    term_id: str = Query(
        "2020-fall",
        title = "Term Code",
        description = "Search for courses in this term; YEAR-SEASON. Ex: Spring Semester = 2021-spring"
    ),
    code: Optional[str] = Query(
        None,
        title = "Course code",
        description = "Unique within the term of a University"
    ),
    title: Optional[str] = Query(
        None,
        title = "Course title",
        description = "A more readable name of a course. Ex: Intro to course"
    ),
    department: Optional[str] = Query(
        None,
        title = "Department code",
        description = "See your university's website for the code. Ex: COMPSCI"
    )

):
    courses = utils.handleUciLiveSearch(request.query_params, term_id=term_id)
    return courses
