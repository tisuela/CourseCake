import pytest
from sqlalchemy.orm import Session

from ...scrapers.course import Course

from .. import crud, models
from ..sql import SessionLocal, engine


class University:

    def __init__(self, name):
        self.name = name

university = University("test1")

@pytest.fixture(scope="module")
def db():
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    models.Base.metadata.drop_all(bind=engine)


def test_add_university(db):
    crud.add_university(db, **university.__dict__)
    universityRow = crud.get_university(db, university.name)
    print("result", universityRow)
    assert universityRow != None



def test_add_course(db):
    course = Course()
    course.name = "test 101"
    course.title = "intro to course"
    course.code = "123456"
    course.department = "test"
    course.type = "lecture"
    course.instructor = "Dr. Test"
    course.time = "time is an illusion"

    course.location = "Testing Hall 200"
    course.building = "Testing Hall"
    course.room  = "200"
    course.status = "OPEN"

    course.units = 4

    course.final = "never"

    course.enrolled = 100
    course.school = "School of Test"
    course.departmentTitle = "Test ing"
    crud.add_course(db, university.name, course)

    courseRow = crud.CourseQuery(db, university.name, {"code[equals]": course.code}).search()[0]

    # courseRow = crud.get_university(db, university.name.upper()).courses.filter(models.Course.__table__.c["code"].in_([course.code])).all()

    print("first thing in course", courseRow)
    assert True
