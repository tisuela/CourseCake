from .uci_class import UciClass
from ..course import Course

class UciScrapeRows:
    '''
    helper class for UciScraper
    Scrapes rows from uci course schedule website
    '''
    def __init__(self, rows: list):
        # list of rows from course table
        self.rows = rows

        # which row we are on
        self.position = 0

        # identifies if a row contains a course
        self.row_contains_class = False
        self.current_course = Course()



        self.courses = dict()

    def match_class(self, htmlTag, s: str):
        return (htmlTag.get("class") != None and htmlTag["class"][0] == s)


    def get_course(self):
        current_row = None

        # Flags to track updates -- it's possible we iterate over two
        # schools, but we onlu want the closest one to our position
        updated_school = False
        updated_department = False
        updated_name_title = False

        # init starting position to iterate over previous rows
        position = self.position - 1

        # how far back we should iterate
        threshold = 12

        # iterate over no more than <threshold> previous rows
        while (position >= 0 and position > self.position - threshold):
            current_row = self.rows[position]

            if (not updated_school and self.match_class(current_row, "college-title")):
                self.current_course.school = current_row.text
                updated_school = True
                # print("ScrapeRows -- get_course -- got school", current_row.text)

            elif (not updated_department and self.match_class(current_row, "dept-title")):
                self.current_course.department_title = current_row.text
                updated_department = True
                # print("ScrapeRows -- get_course -- got dept", current_row.text)


            elif (not updated_name_title) :
                # HTML which contains both the course name and course title
                course_name_title = current_row.find("td", {"class":"CourseTitle"})

                if (course_name_title != None):
                    course_name = " ".join(course_name_title.find(text = True, recursive = False).strip().split())
                    self.current_course.id = course_name.upper()
                    self.current_course.title = course_name_title.find("b").text

                    # Department is the first word in course name
                    self.current_course.department = course_name.rsplit(" ",1)[0].upper()
                    updated_name_title = True
                    # print("ScrapeRows -- get_course -- got name/title", course_name_title.text)


            position -= 1




    def scrape_cells(self, cells):
        '''
        Checks if cells contain course information
        Scrapes cells for course information
        '''
        if self.row_contains_class:
            a_class = UciClass(self.current_course, cells)
            self.current_course.classes.append(a_class)

        else:
            for cell in cells:

                if (cell.text.strip().lower() == "code"):
                    # If this row has the word "Code",
                    # then the next row is a course
                    self.row_contains_class = True

                    new_course = Course(course = self.current_course)
                    self.courses[new_course.id] = new_course

                    self.current_course.classes.clear()
                    # scrape previous rows for the template course info
                    self.get_course()








    def scrape_row(self, row):
        cells = row.findChildren(["th", "td"])

        if (len(cells) > 10):
            self.scrape_cells(cells)

        else:
            self.row_contains_class = False




    def scrape(self):
        '''
        Scrape rows
        '''
        for row in self.rows:
            self.scrape_row(row)

            self.position += 1
