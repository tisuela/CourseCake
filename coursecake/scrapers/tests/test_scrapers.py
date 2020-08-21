# packaging for scrapers.tests


import pytest

from coursecake.scrapers.course_scraper import CourseScraper

def testFunc():
    assert True



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
    courses = scraper.scrape()

    assert len(courses) > 1000
