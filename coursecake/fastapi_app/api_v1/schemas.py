from pydantic import BaseModel


class UniversityBase(BaseModel):
    name: str


class UniversityCreate(UniversityBase):
    pass


class University(UniversityBase):

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    university_name: str
    term_id: str
    code: str


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):

    class Config:
        orm_mode = True
