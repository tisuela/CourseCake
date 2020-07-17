'''
Handles all updates made to database
'''

from .models import Courses,db

from ..scrapers.course_scraper import CourseScraper


def updateAllUCICourses():
    courseScraper = CourseScraper()
    courses = courseScraper.getAllUCICourses()

    for course in courses.values():
        newCourse = Courses(course)
        db.session.merge(newCourse)

    db.session.commit()
