from .universities import Universities
from .course import Course

class Scraper:
    def __init__(self, universityName: str):
        self.universityName = universityName

        # get the course website url
        universities = Universities()
        self.url = universities.getUniversity(self.universityName)

        # list of course
        self.courses = list()

        # flag to identify a course in a table
        self.isCourse = False
