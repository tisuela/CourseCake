# contains all routes for the courses endpoint
from typing import List, Optional
from enum import Enum

from fastapi import Depends, APIRouter, BackgroundTasks, Query, Request
from sqlalchemy.orm import Session

from ....database import crud, models, sql
from ...limiter import limiter
from .. import schemas, structs
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
@limiter.limit("5/second;60/minute;300/hour")
async def all_courses(
    request: Request, offset: int = 0, limit: int = 50, db: Session = Depends(get_db)
):
    courses = crud.get_courses(db, offset=offset, limit=limit)
    return courses


@router.get("/search/{university}", response_model=List[schemas.Course])
@limiter.limit("20/second;60/minute;300/hour")
async def search_courses(
    request: Request,
    university: structs.UniversityName,
    term_id: Optional[str] = Query(
        "2020-fall",
        title="Term Code",
        description="Search for courses in this term; YEAR-SEASON. Ex: Spring Semester = 2021-spring",
    ),
    course_id: Optional[str] = Query(
        None, title="Course code", description="Unique within the term of a University"
    ),
    title: Optional[str] = Query(
        None,
        title="Course title",
        description="A more readable name of a course. Ex: Intro to course",
    ),
    department: Optional[str] = Query(
        None,
        title="Department code",
        description="See your university's website for the code. Ex: COMPSCI",
    ),
    units: Optional[int] = Query(
        None,
        title="Units",
        description="Some (few) courses have variable units. The highest possible units in a course is shown.",
    ),
    prerequistes_str: Optional[str] = Query(
        None,
        title="Prerequisites String",
        description="A String containing a course's prerequisites",
    ),
    department_title: Optional[str] = Query(
        None,
        title="Department Title",
        description="Human-friendly Department name. Ex: Humanities",
    ),
    school: Optional[str] = Query(
        None, title="School", description="Ex: Donald Bren School of Information..."
    ),
    offset: Optional[int] = Query(
        0, description="Use this to see next page of results"
    ),
    limit: Optional[int] = Query(
        50, description="Higher limits can create slower responses"
    ),
    db: Session = Depends(get_db),
):
    courses = crud.CourseQuery(
        db,
        university,
        request.query_params,
        term_id=term_id,
        offset=offset,
        limit=limit,
    ).search()
    return courses
