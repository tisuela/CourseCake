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
    models.Base.metadata.drop_all(bind=engine)


def test_add_university(db):
    crud.add_university(db, **university.__dict__)
    universityRow = crud.get_university(db, university.name)
    print("result", universityRow)
    assert universityRow != None



def test_add_course(db):
    crud.add_course(db, university.name, term_id, course)

    courseRow = crud.CourseQuery(db, university.name, {"code[equals]": course.code}).search()[0]

    # courseRow = crud.get_university(db, university.name.upper()).courses.filter(models.Course.__table__.c["code"].in_([course.code])).all()

    assert True


def test_add_many_course(db):
    '''
    Load testing for adding a course
    '''
    tempCode = course.code
    limit = 900
    new_term_id = "2021-WINTER-1"
    for i in range(limit):
        new_course = Course(course.__dict__)
        new_course.code = tempCode + str(i)
        crud.add_course(db, university.name, new_term_id, new_course, commit = False)

    db.commit()
    courses = crud.CourseQuery(db, university.name,  term_id = new_term_id, limit = limit).search()

    assert len(courses) == limit



def test_bulk_add_courses(db):
    '''
    tests crud.bulk_add_course(db: Session)
    '''
    temp_code = course.code
    limit = 900
    course_list = list()
    new_term_id = "2021-SPRING-1"

    for i in range(limit):
        new_course = Course(course.__dict__)
        new_course.code = str(i) + temp_code
        course_list.append(new_course)

    crud.bulk_add_courses(db, university.name, new_term_id, course_list)
    courses = crud.CourseQuery(db, university.name,  term_id = "2021-SPRING", limit = limit).search()

    assert len(courses) == limit


def test_bulk_merge_courses(db):
    '''
    Load testing for adding a course
    '''
    tempCode = course.code
    limit = 900
    course_list = list()
    new_term_id = "2021-SUMMER-2"

    for i in range(limit):
        new_course = Course(course.__dict__)
        new_course.code = str(i) + tempCode
        course_list.append(new_course)

    crud.bulk_merge_courses(db, university.name, new_term_id, course_list)
    courses = crud.CourseQuery(db, university.name,  term_id = new_term_id, limit = limit).search()

    assert len(courses) == limit
