# uploads courses

from sqlalchemy.orm import Session

from ..scrapers.course import Course
from ..scrapers.course_scraper import CourseScraper

from . import crud, models






def update_all(db: Session, term_id: str = "2020-FALL-1"):
    term_args = term_id.split("-")

    # check if term_id is fully specified
    # if not, fill in assumed values
    if (len(term_args) < 3):
        term_id += "-1"
    university = "uci"
    scraper = CourseScraper().getUciScraper()
    scraper.set_term_id(term_id)
    courses = list(scraper.scrape().values())
    crud.add_university(db, university)
    crud.bulk_merge_courses(db, university, term_id, courses)
