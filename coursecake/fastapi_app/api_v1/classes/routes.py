# contains all routes for the courses endpoint
from typing import List, Optional

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




@router.get("/search/{university}", response_model=List[schemas.Class])
@limiter.limit("20/second;60/minute;300/hour")
async def search_courses(
    request: Request,
    university: structs.UniversityName,
    term_id: Optional[str] = Query(
        "2020-fall",
        title = "Term Code",
        description = "Search for courses in this term; YEAR-SEASON. Ex: Spring Semester = 2021-spring"
    ),
    class_id: Optional[str] = Query(
        None,
        title = "Class id",
        description = "Unique within the term of a University"
    ),
    course_id: Optional[str] = Query(
        None,
        title = "Course id",
        description = "The formal name of a course. Ex: course 101"
    ),
    instructor: Optional[str] = Query(
        None,
        title = "Instructor name",
        description = "Instructor of course. Some courses have multiple instructors"
    ),
    time: Optional[str] = Query(
        None,
        title = "Time",
        description = "Ex: MWF 8am-9:30am"
    ),
    location: Optional[str] = Query(
        None,
        title = "Location",
        description = "Includes building and room info"
    ),
    building: Optional[str] = Query(
        None,
        title = "Building",
        description = "Unique within university"
    ),
    room: Optional[str] = Query(
        None,
        title = "Room",
        description = "Unique within building"
    ),
    status: Optional[str] = Query(
        None,
        title = "Status",
        description = "OPEN / FULL / CLOSED / etc..."
    ),
    units: Optional[int] = Query(
        None,
        title = "Units",
        description = "Some (few) courses have variable units. The highest possible units in a course is shown."
    ),
    enrolled: Optional[int] = Query(
        None,
        title = "Students Enrolled",
    ),
    waitlisted: Optional[int] = Query(
        None,
        title = "Students Waitlisted",
    ),
    requested: Optional[int] = Query(
        None,
        title = "Students that have Requested",
    ),
    max: Optional[int] = Query(
        None,
        title = "Maximum students",
    ),
    offset: Optional[int] = Query(
        0,
        description = "Use this to see next page of results"
    ),
    limit: Optional[int] = Query(
        50,
        description = "Higher limits can create slower responses"
    ),
    db: Session = Depends(get_db)

):
    classes = crud.ClassQuery(db, university, request.query_params, term_id=term_id, offset=offset, limit=limit).search()
    return classes
