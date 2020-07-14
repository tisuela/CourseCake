from .universities import Universities
from .course import Course

class Scraper:
    def __init__(self, universityName: str):
        self.universityName = universityName

        # get the course website url
        universities = Universities()
        self.url = universities.getUniversity(self.universityName)

        # dictionary of course
        self.courses = dict()

        # flag to identify a course in a table
        self.isCourse = False
