# packaging for scrapers.tests
from ..course_scraper import CourseScraper
from ..universities import Universities


def test_add_university():
    universities = Universities()
    uni = "testing"
    course_schedule = "www.google.com"
    course_requisites = "www.elgoog.com"

    universities.add(
        uni,
        **{"course-schedule": course_schedule, "course-requisites": course_requisites}
    )
    info = universities.getUniversity(uni)

    assert info["course-requisites"] == course_requisites


def test_get_departments():
    scraper = CourseScraper().get_scraper("uci")
    departments = scraper.getDepartments()
    assert len(departments) > 5


def testGetCoursesDept():
    scraper = CourseScraper().getUciScraper()
    courses = scraper.getCourses({"department": "compsci"})
    assert len(courses) > 10


def testGetCoursesCode():
    scraper = CourseScraper().getUciScraper()
    courses = scraper.getCourses({"code": "30000-32000"})
    assert len(courses) > 10


def testGetAllCourses():
    scraper = CourseScraper().getUciScraper()
    courses = scraper.scrape(testing=True)
    classes = list()

    classes_are_collected = False
    class_exists = False

    for course in scraper.courses.values():
        classes.extend(course.classes)
        if len(course.classes) > 7:
            classes_are_collected = True

            # for a_class in course.classes:
            #    print(a_class)
            # print(course)

    for a_class in classes:
        if a_class.class_id == "06000":
            class_exists = True

    assert len(courses) > 200
    assert classes_are_collected
    assert class_exists
    assert len(classes) > 1000
