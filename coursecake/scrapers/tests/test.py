# packaging for scrapers.tests


import pytest

from coursecake.scrapers.course_scraper import CourseScraper

def testFunc():
    assert True



def testGetCourses():
    scraper = CourseScraper().getUciScraper()
    courses = scraper.getCourses({"department":"compsci"})
    assert len(courses) > 0
