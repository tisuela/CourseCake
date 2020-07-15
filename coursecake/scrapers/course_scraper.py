from .uci.uci_scraper import UCIScraper
from .course import Course

import json

class CourseScraper:
    '''
    All courses can be scraped from here
    '''
    def __init__(self):

        # Useful to construct other courses using the existing populated
        # attributes from this template
        # Ex: newCourse = Course(self.templateCourse.__dict__)
        self.templateCourse = Course()

    def downloadUCICourses(self):
        courses = UCIScraper().scrape()
        self.downloadCoursesAsJson(courses, "UCICourses.json")


    def downloadCoursesAsJson(self, courses, fileName):
        with open(fileName, "w+") as jsonFile:
            json.dump({"courses": list(course.__dict__ for course in courses.values())}, jsonFile)


        jsonFile.close()


    def getAllUCICourses(self) -> list:
        courses = UCIScraper().getDepartmentCourses("COMPSCI")
        return courses






def main():
    courseScraper = CourseScraper()

    course = Course()
    course.name = "yeet"
    course.code = "1223"
    courses = [course]

    courseScraper.downloadUCICourses()
    # courseScraper.downloadCoursesAsJson(courses, "test.json")



if __name__ == '__main__':
    main()
