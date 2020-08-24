# contains all routes for the courses endpoint
from typing import List, Optional
from enum import Enum

from fastapi import Depends, APIRouter, BackgroundTasks, Query, Request
from sqlalchemy.orm import Session

from ....database import crud, models, sql
from .. import schemas
from . import utils

router = APIRouter()

class UniversityName(str, Enum):
    uci = "uci"
    csus = "csus"


class Term(str, Enum):
    summer_2020_1 = "2020-SUMMER-1"
    summer_2020_2 = "2020-SUMMER-2"
    fall_2020_1 = "2020-FALL"



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
    university: UniversityName,
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


# use CourseBase schema since live search is not as detailed
@router.get("/live-search/{university}", response_model=List[schemas.CourseBase])
async def search_courses(
    request: Request,
    university: UniversityName,
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
