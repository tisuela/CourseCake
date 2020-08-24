'''
Pydantic Schemas model the response for the API -- they are the bridge
between the the database models and the API's JSON responses.
Pydantic Schemas also help generate documentation.

These schemas are based on the models defined in database.models
'''
from datetime import datetime
from pydantic import BaseModel, Field


class UniversityBase(BaseModel):
    name: str


class UniversityCreate(UniversityBase):
    pass


class University(UniversityBase):

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    # primary keys
    university_name: str = Field(..., example="UCI")
    term_id: str = Field(..., example="FALL-2020-1")
    code: str

    name: str
    title: str
    department: str
    instructor: str
    time: str
    location: str
    building: str
    room: str
    status: str
    type: str

    units: int = Field(..., example=4)
    max: int
    enrolled: int
    waitlisted: int
    requested: int

    # optional
    department_title: str
    restrictions: str
    school: str

    updated: datetime


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):

    class Config:
        orm_mode = True
