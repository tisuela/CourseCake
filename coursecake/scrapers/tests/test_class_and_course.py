from ..course_class import CourseClass
from ..course import Course


course = Course()
course.id= "test 101"
course.title = "intro to course"
course.department = "test"
course.units = 4
course.school = "School of Test"
course.department_title = "Test ing"
a_class = None

def test_create_course():
    bad_course = Course()
    assert bad_course.toInt("4") == 4
    bad_course.title = "bas"
    assert not bad_course.is_valid_course()
    new_course = Course(course_dict = course.__dict__)
    assert new_course.id == course.id
    assert new_course.is_valid_course()


def test_create_class():
    global a_class

    a_class = CourseClass(course)
    assert a_class.toInt("4") == 4
    class_id= "12345"
    a_class.id = class_id
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

    assert a_class.isOpen()
    assert a_class.course_id == course.id
    assert a_class.id == class_id
