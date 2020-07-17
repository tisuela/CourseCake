from ..scraper import Scraper
from ..course import Course
from .scraperows import UCIScrapeRows
from bs4 import BeautifulSoup
import requests



class UCIScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self, "UCI")

        # used to specify which term / tear
        self.yearTerm = "2020-92"

        # used for requests to WebSoc
        self.params = {"YearTerm": self.yearTerm, "ShowFinals": 1,
                        "ShowComments": 0}

        # list of department codes (str) for the queries
        self.deptCodes = list()


        # UCI's WebSoc requires that we identify ourselves (User-Agent)
        # The use of session will help for form submissions
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "User"})

        self.getDepartments()
        print("UCIScraper -- initialized")


    def getDepartments(self):
        page = self.session.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")

        # find departments (in the form)
        departments = soup.find("select", {"name": "Dept"}).findChildren("option")
        for dept in departments:
            # print("UCIScraper -- getDepartments --", dept["value"])

            # getting ALL as a dept will lead to an error
            if (dept["value"].strip() != "ALL"):
                self.deptCodes.append(dept["value"])

        print("UCIScraper -- getDepartments --","Departments initialized")



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

                rowsScraper = UCIScrapeRows(rows)
                rowsScraper.scrape()
                courses.update(rowsScraper.courses)




        except IndexError:
            # index error means no course list was in the page
            # We want to print out the error message
            print("UCIScraper -- scrapePage --","ERROR:", soup.find("div", {"style":"color: red; font-weight: bold;"}).text.strip())
        return courses





    def getCoursesByDepartment(self) -> list:
        courses = dict()
        for dept in self.deptCodes:
            print("UCIScraper -- getCoursesByDepartment --", "scraping", dept)

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
            print("UCIScraper -- getCoursesByCourseCodes --", "scraping", courseCodes)

            courses.update(self.getCourseCodeCourses(courseCodes))

            lowerBound = upperBound + 1
            upperBound += increment


        return courses



    def scrape(self) -> list:
        '''
        Gets all UCI courses
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
