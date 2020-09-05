import requests
from bs4 import BeautifulSoup

from ..scraper import Scraper
from ..course import Course
from .scraperows import UciScrapeRows




class UciScraper(Scraper):
    # from our defined query params to WebSoc's params
    PARAM_ENCODER ={
        "days": "Days",
        "yearterm": "YearTerm",
        "units": "Units",
        "title": "CourseTitle",
        "starttime": "StartTime",
        "endtime": "EndTime",
        "breadth": "Breadth",
        "instructor": "InstrName",
        "division": "Division",
        "department": "Dept",
        "code": "CourseCodes"
    }

    REQUIRED_PARAMS = [
        "breadth",
        "instructor",
        "code",
        "dept"
    ]

    YEAR_TERM_ENCODER = {
        "2020-SUMMER-1": "2020-51",
        "2020-SUMMER-2": "2020-76",
        "2020-FALL-1": "2020-92"
    }

    def __init__(self, term_id: str = "2020-FALL-1"):
        Scraper.__init__(self, "UCI", term_id)

        self.url = self.urls["course-schedule"]

        # used to specify which term / tear
        self.year_term = self.YEAR_TERM_ENCODER[self.term_id]

        # used for requests to WebSoc
        self.params = {"YearTerm": self.year_term, "ShowFinals": 1,
                        "ShowComments": 1}

        # list of department codes (str) for the queries
        self.deptCodes = list()

        # Uci's WebSoc requires that we identify ourselves (User-Agent)
        # The use of session will help for form submissions
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "User"})


        print("UciScraper -- initialized")


    def set_term_id(self, term_id: str) -> None:
        self.term_id = term_id.upper()
        self.year_term = self.YEAR_TERM_ENCODER[self.term_id]
        self.params["YearTerm"] = self.year_term


    def getDepartments(self) -> list:
        page = self.session.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")

        # find departments (in the form)
        departments = soup.find("select", {"name": "Dept"}).findChildren("option")
        for dept in departments:
            # print("UciScraper -- getDepartments --", dept["value"])

            # getting ALL as a dept will lead to an error
            if (dept["value"].strip() != "ALL"):
                self.deptCodes.append(dept["value"])

        return self.deptCodes


    def getCourses(self, args: dict) -> dict:
        '''
        Retrieves list of courses by dynamically
        building the request params
        '''
        params = dict()
        for arg in args:
            try:
                encodedParam = self.PARAM_ENCODER[arg]
                params[encodedParam] = args[arg].upper()
            except KeyError:
                print(f"uci_scraper -- getCourses -- invalid arg {arg}")

        params.update(self.params)
        page = self.session.get(self.url, params = params)
        courses = self.scrapePage(page)

        return courses



    def getCourseCodeCourses(self, courseCodes: str) -> dict:
        '''
        Retrieves list of courses by querying course codes
        i.e. 30000-35000 or 32140
        '''
        params = {"CourseCodes": courseCodes}

        # add the base params
        params.update(self.params)
        page = self.session.get(self.url, params = params)
        courses = self.scrapePage(page)

        return courses

    def merge_courses(self, src: dict, target: dict) -> dict:
        '''
        It's possible that a course's classes can be spread out between
        two pages when iterating over the courses, ending up in duplicate
        keys and lost information

        this method merges two course dicts to find duplicate keys and merge
        their class lists to ensure no information is lost

        target is the dict where we want the values to be added/merged to

        src contains the new values u want to add

        This "merges" the information into the newer dict; src.
        It returns the new dict, which u then want to ADD to the target dict.
        SO basically, this doesn't do all the work
        '''

        target_keys = set(target.keys())

        for src_key in src:
            if src_key in target_keys:
                src[src_key].classes.extend(target[src_key].classes)


        return src



    def scrapePage(self, page) -> dict:
        # Get course table
        courses = dict()
        soup = BeautifulSoup(page.content, "lxml")

        try:
            courseTables = soup.find("div", {"class": "course-list"}).findChildren("table")

            for table in courseTables:
                rows = table.findChildren("tr")

                rowsScraper = UciScrapeRows(rows)
                rowsScraper.scrape()
                courses.update(rowsScraper.courses)

        except IndexError:
            # index error means no course list was in the page
            # We want to print out the error message
            print("UciScraper -- scrapePage --","ERROR:", soup.find("div", {"style":"color: red; font-weight: bold;"}).text.strip())
        return courses



    def getCoursesByCourseCodes(self, max: int = 99999) -> list:
        '''
        Gets courses by searching through ranges of codes

        i.e. 0-3000, then 3001-4000, ... etc.

        For efficiency, we query codes in predefined increments.
        WebSoc throws an error when a query has > 900 courses
        '''
        courses = dict()

        # define the course code range to search
        lowerBound = 0
        upperBound = 3000
        increment = upperBound - lowerBound


        while (lowerBound < max):

            if (upperBound > max):
                # we need to be able to get course code 99999, but
                # anything above that course code will give an error
                upperBound = max

            courseCodes = f"{lowerBound}-{upperBound}"
            print("UciScraper -- getCoursesByCourseCodes --", "scraping", courseCodes)

            courses.update(self.merge_courses(self.getCourseCodeCourses(courseCodes), courses))

            lowerBound = upperBound + 1
            upperBound += increment


        return courses



    def scrape(self, testing: bool = False) -> dict:
        '''
        Gets all Uci courses
        '''
        # self.getCoursesByDepartment()
        if testing:
            self.courses = self.getCoursesByCourseCodes(max = 10000)
        else:
            self.courses = self.getCoursesByCourseCodes()

        return self.courses


'''
Alternative:
    import urllib.request as urllib

    request = urllib.Request("https://www.reg.uci.edu/perl/WebSoc/")
    request.add_header('User-Agent', 'poop')

    #open page
    open = urllib.urlopen(request)

    page = BeautifulSoup(open, "lxml")


'''
