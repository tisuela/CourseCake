from ..course_class import CourseClass
from ..course import Course


course = Course()
course.code = "test 101"
course.title = "intro to course"
course.department = "test"
course.units = 4
course.school = "School of Test"
course.department_title = "Test ing"
a_class = None

def test_create_course():
    new_course = Course(course.__dict__)
    assert new_course.code == course.code


def test_create_class():
    global a_class

    a_class = CourseClass(course)
    class_code = "12345"
    a_class.code = class_code
    a_class.type = "lecture"
    a_class.instructor = "Dr. Test"
    a_class.time = "time is an illusion"

    a_class.location = "Testing Hall 200"
    a_class.building = "Testing Hall"
    a_class.room  = "200"
    a_class.status = "OPEN"

    a_class.units = 4

    a_class.final = "never"

    a_class.enrolled = 100

    assert a_class.course_code == course.code
    assert a_class.code == class_code
