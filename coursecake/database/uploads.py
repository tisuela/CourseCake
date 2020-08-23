# uploads courses

from sqlalchemy.orm import Session

from ..scrapers.course import Course
from ..scrapers.course_scraper import CourseScraper

from . import crud, models






def update_all(db: Session):
    university = "uci"
    scraper = CourseScraper()
    courses = list(scraper.getAllUciCourses().values())
    crud.add_university(db, university)
    crud.bulk_merge_courses(db, university, "2020-FALL-1", courses)
