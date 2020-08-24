from ..scraper import Scraper
from ..course import Course
from .scraperows import UciScrapeRows
from bs4 import BeautifulSoup
import requests



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


    def getDepartments(self):
        page = self.session.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")

        # find departments (in the form)
        departments = soup.find("select", {"name": "Dept"}).findChildren("option")
        for dept in departments:
            # print("UciScraper -- getDepartments --", dept["value"])

            # getting ALL as a dept will lead to an error
            if (dept["value"].strip() != "ALL"):
                self.deptCodes.append(dept["value"])

        print("UciScraper -- getDepartments --","Departments initialized")


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



    def getDepartmentCourses(self, dept: str) -> dict:
        '''
        Retrieves list of courses by querying department name
        '''

        # use params to "submit" the form data
        # (but for simplicity, we aren't using the form)
        params = {"Dept": dept}

        # add the base params
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





    def getCoursesByDepartment(self) -> list:
        courses = dict()
        self.getDepartments()
        for dept in self.deptCodes:
            print("UciScraper -- getCoursesByDepartment --", "scraping", dept)

            courses.update(self.getDepartmentCourses(dept))

        return courses



    def getCoursesByCourseCodes(self) -> list:
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
        max = 99999

        while (lowerBound < max):

            if (upperBound > max):
                # we need to be able to get course code 99999, but
                # anything above that course code will give an error
                upperBound = max

            courseCodes = f"{lowerBound}-{upperBound}"
            print("UciScraper -- getCoursesByCourseCodes --", "scraping", courseCodes)

            courses.update(self.getCourseCodeCourses(courseCodes))

            lowerBound = upperBound + 1
            upperBound += increment


        return courses



    def scrape(self) -> dict:
        '''
        Gets all Uci courses
        '''
        # self.getCoursesByDepartment()
        self.courses = self.getCoursesByCourseCodes()

        return self.courses



    def toInt(self, s: str) -> int:
        try:
            return int(s)
        except ValueError:
            return -1














def main():

    '''
    for course in scraper.courses:
        print(course)
    '''

if __name__ == '__main__':
    main()



'''
Alternative:
    import urllib.request as urllib

    request = urllib.Request("https://www.reg.uci.edu/perl/WebSoc/")
    request.add_header('User-Agent', 'poop')

    #open page
    open = urllib.urlopen(request)

    page = BeautifulSoup(open, "lxml")


'''
