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
        **{"course-schedule": course_schedule,
            "course-requisites": course_requisites
        }
    )
    info = universities.getUniversity(uni)

    assert info["course-requisites"] == course_requisites

def test_get_departments():
    scraper = CourseScraper().getUciScraper()
    departments = scraper.getDepartments()
    assert len(departments) > 5

def testGetCoursesDept():
    scraper = CourseScraper().getUciScraper()
    courses = scraper.getCourses({"department":"compsci"})
    assert len(courses) > 10


def testGetCoursesCode():
    scraper = CourseScraper().getUciScraper()
    courses = scraper.getCourses({"code": "30000-32000"})
    assert len(courses) > 10


def testGetAllCourses():
    scraper = CourseScraper().getUciScraper()
    courses = scraper.scrape(testing = True)

    assert len(courses) > 1000
