from .universities import Universities
from .course import Course


class Scraper:
    def __init__(self, universityName: str, term_id: str):
        self.universityName = universityName
        self.term_id = term_id.upper()

        # get the course website url
        universities = Universities()
        self.urls = universities.getUniversity(self.universityName)

        # dictionary of course
        self.courses = dict()

        # at least one of these params needed to query scraper
        self.requiredParams = list()

    def getCourses(self, args: dict) -> dict:
        """
        Needs implementation by child
        """
        courses = dict()
        return courses

    def scrape(self) -> dict:
        """
        Implemented by child
        """
        return self.courses
