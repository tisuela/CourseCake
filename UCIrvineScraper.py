import Universities
from Course import Course

from bs4 import BeautifulSoup
import requests



class Scraper:
    def __init__(self):
        # get the course website url
        self.url = Universities.Universities().getUniversity("UCIrvine")

        # used to specify which term / tear
        self.yearTerm = "2020-92"

        # list of department codes (str) for the queries
        self.deptCodes = list()

        # flag to identify a course in a table
        self.isCourse = False

        # A list of Course (not used at the moment)
        self.courses = list()

        # UCI's WebSoc requires that we identify ourselves (User-Agent)
        # The use of session will help for form submissions
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "User"})

        self.getDepartments()
        print("UCIrvineScraper -- initialized")


    def getDepartments(self):
        page = self.session.get(self.url)
        soup = BeautifulSoup(page.content, "lxml")

        # find departments (in the form)
        departments = soup.find("select", {"name": "Dept"}).findChildren("option")
        for dept in departments:
            # print("UCIrvineScraper -- getDepartments --", dept["value"])

            # getting ALL as a dept will lead to an error
            if (dept["value"].strip() != "ALL"):
                self.deptCodes.append(dept["value"])

        print("UCIrvineScraper -- getDepartments --","Departments initialized")


    def getDepartmentCourses(self, dept: str) -> list:
        '''
        Retrieves list of courses by querying department name
        '''

        # use params to "submit" the form data
        # (but for simplicity, we aren't using the form)
        params = {"YearTerm": self.yearTerm, "Dept": dept}
        page = self.session.get(self.url, params = params)
        courses = self.scrapePage(page)

        return courses


    def getCourseCodeCourses(self, courseCodes: str) -> list:
        '''
        Retrieves list of courses by querying course codes
        i.e. 30000-35000 or 32140
        '''
        params = {"YearTerm": self.yearTerm, "CourseCodes": courseCodes}
        page = self.session.get(self.url, params = params)
        courses = self.scrapePage(page)

        return courses



    def scrapePage(self, page) -> list:
        # Get course table
        courses = list()
        soup = BeautifulSoup(page.content, "lxml")

        try:
            courseTable = soup.find("div", {"class": "course-list"}).findChildren("table")[0]
            rows = courseTable.findChildren("tr")


            # flag to identify a valid course row
            rowIsCourse = False
            for row in rows:
                courses.extend(self.scrapeRow(row))

        except IndexError:
            # index error means no course list was in the page
            # We want to print out the error message
            print("UCIrvineScraper -- scrapePage --", soup.find("div", {"style":"color: red; font-weight: bold;"}).text.strip())
        return courses


    def scrapeRow(self, row) -> list:
        courses = list()
        cells = row.findChildren(["th", "td"])

        # make sure this is a valid row
        if (len(cells) > 10):
            if self.isCourse:
                course = self.scrapeCells(cells)
                courses.append(course)

            else:
                for cell in cells:
                    if (cell.text.strip().lower() == "code"):
                        # If this row has the word "Code",
                        # then the next row is a course
                        self.isCourse = True

        elif (len(cells) > 4):
            # if this row doesn't contain a course and has more than four cells
            # It usually contains data about the course from the previous row
            # But we'll ignore it for now
            pass

        elif (len(cells) < 2):
            # if this row is invalid (less than 2 cells), the next row is not a course
            self.isCourse = False

        return courses



    def scrapeCells(self, cells) -> Course:
        course = Course()
        course.code = cells[0].text
        course.instructor = cells[4].text
        course.location = cells[6].text

        # print("UCIrvineScraper -- scrapeCells --", "added course", course)

        return course



    def getCoursesByDepartment(self) -> list:
        courses = list()
        for dept in self.deptCodes:
            print("UCIrvineScraper -- getCoursesByDepartment --", "scraping", dept)

            courses.extend(self.getDepartmentCourses(dept))

        return courses



    def getCoursesByCourseCodes(self) -> list:
        '''
        Gets courses by searching through ranges of codes

        i.e. 0-3000, then 3001-4000, ... etc.

        For efficiency, we query codes in predefined increments.
        WebSoc throws an error when a query has > 900 courses
        '''
        courses = list()

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
            print("UCIrvineScraper -- getCoursesByCourseCodes --", "scraping", courseCodes)
            self.getCourseCodeCourses(courseCodes)

            lowerBound = upperBound + 1
            upperBound += increment



    def scrape(self):
        # self.getCoursesByDepartment()
        self.getCoursesByCourseCodes()














def main():
    scraper = Scraper()
    scraper.scrape()
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
