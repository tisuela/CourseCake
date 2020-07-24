'''
Handles all admin updates made to database
'''

from ..models import Courses, University, db

from ...scrapers.course_scraper import CourseScraper


def updateAllUciCourses():
    courseScraper = CourseScraper()
    courses = courseScraper.getAllUciCourses()

    uni = University("UCI")
    db.session.merge(uni)

    for course in courses.values():
        newCourse = Courses(course, "UCI")
        db.session.merge(newCourse)

    db.session.commit()


def reloadCoursesModel():
    Courses.__table__.drop(db.engine)
    db.create_all()


def reloadUniversityModel():
    University.__table__.drop(db.engine)
    db.create_all()


def reloadAllModels():
    db.drop_all()
    db.create_all()
