'''
Handles all admin updates made to database
'''

from ..models import Courses,db

from ...scrapers.course_scraper import CourseScraper


def updateAllUciCourses():
    courseScraper = CourseScraper()
    courses = courseScraper.getAllUciCourses()

    for course in courses.values():
        newCourse = Courses(course)
        db.session.merge(newCourse)

    db.session.commit()
