from .universities import Universities
from .course import Course



class InvalidTermId(Exception):
    def __init__(self, term_id: str, encoded_term_id: str = None):
        self.term_id = term_id
        self.encoded_term_id = encoded_term_id

    def __str__(self):

        return (
            f"Invalid Term Id, {self.term_id}"
            + f" Encoded Term Id, {self.encoded_term_id} did not"
            + " match with any supported term in the scraper"
        )

class Scraper:
    def __init__(self, universityName: str, term_id: str):
        self.universityName = universityName
        self.term_id = term_id.upper()

        # get the course website url
        universities = Universities()
        self.urls = universities.getUniversity(self.universityName)

        # dictionary of course
        self.courses = dict()


        self.classees = dict()

        # at least one of these params needed to query scraper
        self.requiredParams = list()

    def get_classes(self) -> dict:
        """
        Needs implementation by child
        """
        courses = dict()
        return courses

    def get_courses(self) -> dict:
        """
        Needs implementation by child
        """
        courses = dict()
        return courses
