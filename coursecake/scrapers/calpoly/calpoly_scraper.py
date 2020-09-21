import requests
from bs4 import BeautifulSoup, NavigableString

from ..scraper import Scraper, InvalidTermId
from ..course import Course
from ..course_class import CourseClass
from .constants import (
    BASE_URL,
    BASE_HEADERS,
    DEPARTMENTS,
    SEARCH_FORM_DATA,
    CONFIRM_FORM_DATA,
    TERMS_FORM_DATA,
)


class CalpolyScraper(Scraper):
    def __init__(self, term_id: str = "2020-FALL-1"):
        Scraper.__init__(self, "calpoly", term_id)
        self.session = requests.Session()
        self.session.headers = BASE_HEADERS
        self.term_encoder = self.__init_terms()

        try:
            self.term_code = self.term_encoder[self.term_id]
        except KeyError:
            raise InvalidTermId(self.term_id)

    def __init_terms(self):
        term_encoder = dict()

        initial_response = self.session.get(BASE_URL)
        terms_response = self.session.post(BASE_URL, data=TERMS_FORM_DATA)

        terms_page = BeautifulSoup(terms_response.content, "lxml")
        terms_table = terms_page.find_all("table", id="PTSRCHRESULTS")[-1]

        for row in terms_table.children:
            if not isinstance(row, NavigableString):
                cells = row.find_all("td")
                if len(cells) > 2:
                    term_info = cells[1].text.strip().upper().split()

                    # Our unique identifier for a term
                    term_id = f"{term_info[2]}-{term_info[0]}-1"

                    # calpoly's unique identifier for a term
                    term_code = cells[0].text.strip()
                    term_encoder[term_id] = term_code

        return term_encoder

    def scrape_class_status(self, cell) -> str:
        src = cell.find("img")["src"].upper()

        if "OPEN" in src:
            return "OPEN"
        elif "CLOSED" in src:
            return "CLOSED"
        elif "WAITLIST" in src:
            return "WAITLIST"

        # return None if invalid src
        return None

    def scrape_classes_table(self, table, course: Course) -> Course:
        for row in table.find_all("tr", recursive=False):
            cells = row.find_all("td", recursive=False)

            # check if this is actually the cells containing course info
            if len(cells) > 2:
                a_class = CourseClass(course)
                a_class.class_id = cells[0].text.strip()

                # get days and time
                days_times = cells[2].text.strip().split(" ", 1)
                a_class.days = days_times[0].strip()
                a_class.time = days_times[-1].strip()

                # get location info
                a_class.location = cells[3].text.strip()
                building_room = cells[3].text.rsplit(" ", 1)
                a_class.building = building_room[0]
                a_class.room = building_room[-1]

                a_class.instructor = cells[4].text.strip()

                a_class.status = self.scrape_class_status(cells[-1])

                course.classes.append(a_class)

                self.classes[a_class.class_id] = a_class

        return course

    def scrape_classes_page(self, page, department: str):
        """
        Scrape classes from calpoly schedule of classes web page
        """
        soup = BeautifulSoup(page.content, "lxml")
        course = None

        for table in soup.find_all("table", class_="PSGROUPBOXWBO")[-1].find_all(
            "table"
        ):

            # get the course cell which precedes class schedule info
            course_cell = table.find("tr", recursive=False).find(
                "td", class_="PAGROUPBOXLABELLEVEL1", recursive=False
            )

            if course_cell is not None:
                course_label = course_cell.text

                # Get course info
                # Lots of whitespace to be removed
                course_info = course_label.strip().split("-")
                course_id_info = course_info[0].strip().split()

                course = Course()
                course.course_id = f"{course_id_info[0]} {course_id_info[-1]}"
                course.title = course_info[-1].strip()
                course.department = department

            # look for the class table
            if table["class"][0].strip() == "PSLEVEL1GRIDNBONBO":
                self.scrape_classes_table(table, course)
                self.courses[course.course_id] = course

    def get_classes(self, testing: bool = False, term_code: str = None) -> dict:
        test_limit = 1

        if term_code == None:
            term_code = self.term_code

        # add term form data to post requests
        term_form_data = {"SLO_SS_DERIVED_STRM": term_code}
        search_body = SEARCH_FORM_DATA
        confirm_body = CONFIRM_FORM_DATA
        search_body.update(term_form_data)
        confirm_body.update(term_form_data)

        for i in range(len(DEPARTMENTS)):
            department = DEPARTMENTS[i]
            # each department search needs to start with a get request
            # this allows for a "clean" page, since each page is
            # dynamically generated by AJAX
            first_response = self.session.get(BASE_URL)

            body = SEARCH_FORM_DATA
            body.update({"SSR_CLSRCH_WRK_SUBJECT_SRCH$0": department})

            search_response = self.session.post(BASE_URL, data=search_body)

            # check if this window is a confirmation page
            if "SSR_CLSRCH_ENTRY" in search_response.text[:100]:

                # send confirmation to get the actual search response
                search_response = self.session.post(BASE_URL, data=confirm_body)
                print(f"finished {department}")

            self.scrape_classes_page(search_response, department)

            # terminate loop early for tests
            if testing:
                if i + 1 > test_limit:
                    break

        return self.courses
