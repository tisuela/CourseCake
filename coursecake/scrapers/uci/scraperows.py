from .uci_course import UciCourse
from ..course import Course

class UciScrapeRows:
    def __init__(self, rows: list):
        # list of rows from course table
        self.rows = rows

        # which row we are on
        self.position = 0

        # identifies if a row contains a course
        self.rowContainsCourse = False
        self.templateCourse = Course()


        self.courses = dict()

    def matchClass(self, htmlTag, s: str):
        return (htmlTag.get("class") != None and htmlTag["class"][0] == s)


    def getTemplateCourse(self):
        currentRow = None

        # Flags to track updates -- it's possible we iterate over two
        # schools, but we onlu want the closest one to our position
        updatedSchool = False
        updatedDepartment = False
        updatedNameTitle = False

        # init starting position to iterate over previous rows
        position = self.position - 1

        # how far back we should iterate
        threshold = 12

        # iterate over no more than <threshold> previous rows
        while (position >= 0 and position > self.position - threshold):
            currentRow = self.rows[position]

            if (not updatedSchool and self.matchClass(currentRow, "college-title")):
                self.templateCourse.school = currentRow.text
                updatedSchool = True
                # print("ScrapeRows -- getTemplateCourse -- got school", currentRow.text)

            elif (not updatedDepartment and self.matchClass(currentRow, "dept-title")):
                self.templateCourse.departmentTitle = currentRow.text
                updatedDepartment = True
                # print("ScrapeRows -- getTemplateCourse -- got dept", currentRow.text)


            elif (not updatedNameTitle) :
                # HTML which contains both the course name and course title
                courseNameTitle = currentRow.find("td", {"class":"CourseTitle"})

                if (courseNameTitle != None):
                    courseName = " ".join(courseNameTitle.find(text = True, recursive = False).strip().split())
                    self.templateCourse.name = courseName.upper()
                    self.templateCourse.title = courseNameTitle.find("b").text

                    # Department is the first word in course name
                    self.templateCourse.department = courseName.rsplit(" ",1)[0].upper()
                    updatedNameTitle = True
                    # print("ScrapeRows -- getTemplateCourse -- got name/title", courseNameTitle.text)


            position -= 1




    def scrapeCells(self, cells):
        '''
        Checks if cells contain course information
        Scrapes cells for course information
        '''
        if self.rowContainsCourse:
            course = UciCourse(cells, templateCourse =  self.templateCourse)
            self.courses[course.code] = course

        else:
            for cell in cells:

                if (cell.text.strip().lower() == "code"):
                    # If this row has the word "Code",
                    # then the next row is a course
                    self.rowContainsCourse = True

                    # scrape previous rows for the template course info
                    self.getTemplateCourse()






    def scrapeRow(self, row):
        cells = row.findChildren(["th", "td"])

        if (len(cells) > 10):
            self.scrapeCells(cells)

        else:
            self.rowContainsCourse = False




    def scrape(self) -> dict:
        '''
        Scrape rows and return dict of courses
        '''
        for row in self.rows:
            self.scrapeRow(row)

            self.position += 1
