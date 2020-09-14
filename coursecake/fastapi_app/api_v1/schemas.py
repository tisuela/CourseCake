"""
Pydantic Schemas model the response for the API, which is enforces OpenAPI
standards.
They are the bridge between the the database models and the API's JSON
responses.
Pydantic Schemas also help generate documentation.

These schemas are based on the models defined in database.models
"""
from typing import List
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
    """
    Used by live-search
    """

    # primary keys
    course_id: str

    title: str
    department: str

    units: int = Field(..., example=4)

    # optional
    prerequisites_str: str
    department_title: str
    restrictions: str
    school: str

    provider: str = Field(..., example="SlugSurvival")

    class Config:
        orm_mode = True


class CourseCreate(CourseBase):
    """
    All Course inserts need these additional primary keys
    """

    # primary keys
    university_name: str = Field(..., example="UCI")
    term_id: str = Field(..., example="FALL-2020-1")

    updated: datetime


class ClassBase(BaseModel):
    """
    Used by live-search
    """

    # primary keys
    class_id: str

    course_id: str
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

    provider: str = Field(..., example="SlugSurvival")

    class Config:
        orm_mode = True


class Course(CourseBase):
    """
    All Course reads from the database carry more information
    """

    # primary keys
    university_name: str = Field(..., example="UCI")
    term_id: str = Field(..., example="FALL-2020-1")
    updated: datetime
    classes: List[ClassBase] = []

    class Config:
        orm_mode = True


class ClassCreate(ClassBase):
    """
    All Course reads from the database carry more information
    """

    # primary keys
    university_name: str = Field(..., example="UCI")
    term_id: str = Field(..., example="FALL-2020-1")
    updated: datetime

    class Config:
        orm_mode = True


class Class(ClassBase):
    """
    All Course reads from the database carry more information
    """

    # primary keys
    university_name: str = Field(..., example="UCI")
    term_id: str = Field(..., example="FALL-2020-1")
    updated: datetime
    course: CourseBase

    class Config:
        orm_mode = True
