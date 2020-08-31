'''
Pydantic Schemas model the response for the API, which is enforces OpenAPI
standards.
They are the bridge between the the database models and the API's JSON
responses.
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
    '''
    Used by live-search
    '''
    # primary keys
    id: str

    title: str
    department: str


    units: int = Field(..., example=4)

    # optional
    department_title: str
    restrictions: str
    school: str




class CourseCreate(CourseBase):
    '''
    All Course inserts need these additional primary keys
    '''
    # primary keys
    university_name: str = Field(..., example="UCI")
    term_id: str = Field(..., example="FALL-2020-1")

    updated: datetime
    pass


class Course(CourseBase):
    '''
    All Course reads from the database carry more information
    '''
    # primary keys
    university_name: str = Field(..., example="UCI")
    term_id: str = Field(..., example="FALL-2020-1")
    class Config:
        orm_mode = True



class ClassBase(BaseModel):
    '''
    Used by live-search
    '''
    # primary keys
    id: str

    course_id: str
    instructor: str


    units: int = Field(..., example=4)


class Class(ClassBase):
    '''
    All Course reads from the database carry more information
    '''
    # primary keys
    university_name: str = Field(..., example="UCI")
    term_id: str = Field(..., example="FALL-2020-1")
    class Config:
        orm_mode = True
