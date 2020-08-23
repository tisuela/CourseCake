import pytest
from sqlalchemy.orm import Session

from ...scrapers.course import Course

from .. import crud, models
from ..sql import SessionLocal, engine


class University:

    def __init__(self, name):
        self.name = name

university = University("test1")
term_id = "2020-FALL-1"

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
course.department_title = "Test ing"



@pytest.fixture(scope="module")
def db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    # models.Base.metadata.drop_all(bind=engine)


def test_add_university(db):
    crud.add_university(db, **university.__dict__)
    universityRow = crud.get_university(db, university.name)
    print("result", universityRow)
    assert universityRow != None



def test_add_course(db):
    crud.add_course(db, university.name, term_id, course)

    courseRow = crud.CourseQuery(db, university.name, {"code[equals]": course.code}).search()[0]

    # courseRow = crud.get_university(db, university.name.upper()).courses.filter(models.Course.__table__.c["code"].in_([course.code])).all()

    print("first thing in course", courseRow)
    assert True


def test_add_many_course(db):
    '''
    Load testing for adding a course
    '''
    tempCode = course.code
    limit = 900
    for i in range(limit):
        newCourse = Course(course.__dict__)
        newCourse.code = tempCode + str(i)
        crud.add_course(db, university.name, term_id, newCourse, commit = False)

    db.commit()
    courses = crud.get_courses(db, limit = limit)

    assert len(courses) >= limit



def test_bulk_add_courses(db):
    '''
    tests crud.bulk_add_course(db: Session)
    '''
    tempCode = course.code
    limit = 900
    courseList = list()

    for i in range(limit):
        newCourse = Course(course.__dict__)
        newCourse.code = str(i) + tempCode
        courseList.append(newCourse)

    print("created course list, now bulk inserting")

    crud.bulk_add_courses(db, university.name, term_id, courseList)


    courses = crud.get_courses(db, limit = limit)

    assert len(courses) >= limit


def test_bulk_merge_courses(db):
    '''
    Load testing for adding a course
    '''
    tempCode = course.code
    limit = 900
    courseList = list()

    for i in range(limit):
        newCourse = Course(course.__dict__)
        newCourse.code = str(i) + tempCode
        courseList.append(newCourse)

    print("created course list, now bulk inserting")

    crud.bulk_merge_courses(db, university.name, term_id, courseList)

    courses = crud.get_courses(db, limit = limit)

    assert len(courses) >= limit
