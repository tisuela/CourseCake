# Data provider is a student-made REST API: SlugSurvival
# https://slugsurvival.com/explain/opensource
import requests

from ..course import Course
from ..course_class import CourseClass
from ..scraper import Scraper
from .constants import TERMS_API_URL, CLASSES_API_BASE_URL


class InvalidTermId(Exception):
    def __init__(self, term_id: str, encoded_term_id: str):
        self.term_id = term_id
        self.encoded_term_id = encoded_term_id

    def __str__(self):

        return (
            f"Invalid Term Id, {self.term_id}"
            + f" Encoded Term Id, {self.encoded_term_id} did not"
            + " match with any term name found in SlugSurvival"
        )


class UcscScraper(Scraper):
    def __init__(self, term_id: str = "2020-FALL-1"):
        Scraper.__init__(self, "UCSC", term_id)
        self.encoded_term_id = self._encode_term_id(term_id)

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "User"})

        # get term code as defined in SlugSurvival
        self.term_code = self._get_term_code(self.encoded_term_id)

    def _encode_term_id(self, term_id: str):
        """
        Encodes the term_id so we can match it with a term code
        in SlugSurvival's endpoints
        """
        term_info = term_id.split("-")
        encoded = f"{term_info[0]} {term_info[1]} QUARTER"
        return encoded

    def _get_term_code(self, encoded_term_id: str):
        """
        Gets the SlugSurvival term code by matching our
        encoded_term_id with SlugSurvival's term name
        """
        term_response = self.session.get(TERMS_API_URL)
        terms = term_response.json()

        for term in terms:
            if term["name"].upper() == encoded_term_id.upper():
                return term["code"]

        # Raise error if term not found
        raise InvalidTermId(self.term_id, encoded_term_id)

    def get_classes(self, testing: bool = False, term_code: str = None) -> dict:
        """
        Gets all courses (base information) + classes from
        SlugSurvival.

        Populates self.courses and also returns a list of classees
        """
        # default term_code is the attribute stored in class after __init__
        if term_code == None:
            term_code = self.term_code

        url = f"{CLASSES_API_BASE_URL}{term_code}.json"
        classes_response = self.session.get(url)
        class_info = classes_response.json()
        classes = list()

        for department in class_info:
            for a_class in class_info[department]:
                # print(a_class)
                course_id = f"{department} {a_class['c']}"

                # if course is new, add it to the course dict
                if course_id not in self.courses:
                    new_course = Course()
                    new_course.provider = "SlugSurvival https://slugsurvival.com/"
                    new_course.course_id = course_id
                    new_course.title = a_class["n"]
                    new_course.department = department
                    self.courses[course_id] = new_course

                new_class = CourseClass(self.courses[course_id])
                new_class.provider = "SlugSurvival https://slugsurvival.com/"
                new_class.class_id = a_class["num"]
                new_class.instructor = ";".join(a_class["ins"]["d"])
                new_class.location = a_class["loct"][0]["loc"]

                if len(new_class.location) < 1:
                    new_class.building = ""
                    new_class.room = ""
                else:
                    new_class.building = new_class.location.split()[0]
                    new_class.room = new_class.location.split()[-1]

                if not isinstance(a_class["loct"][0]["t"], str):
                    new_class.days = [""]
                    new_class.time = ""
                else:
                    new_class.days = list(
                        day.upper() for day in a_class["loct"][0]["t"]["day"]
                    )
                    new_class.time = (
                        f'{a_class["loct"][0]["t"]["time"]["start"]}-'
                        + f'{a_class["loct"][0]["t"]["time"]["end"]}'
                    )

                self.courses[course_id].classes.append(new_class)
                classes.append(new_class)

        return classes
