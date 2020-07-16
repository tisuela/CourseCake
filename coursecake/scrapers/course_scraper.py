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

    def getAllUCICourses(self) -> dict:
        courses = UCIScraper().scrape()

        # courses = UCIScraper().getDepartmentCourses("COMPSCI")
        return courses


    def downloadUCICourses(self):
        courses = self.getAllUCICourses()
        self.downloadCoursesAsJson(courses, "UCICourses.json")


    def downloadCoursesAsJson(self, courses, fileName):
        with open(fileName, "w+") as jsonFile:
            json.dump({"courses": list(course.__dict__ for course in courses.values())}, jsonFile)


        jsonFile.close()








def main():
    courseScraper = CourseScraper()


    courseScraper.downloadUCICourses()
    # courseScraper.downloadCoursesAsJson(courses, "test.json")



if __name__ == '__main__':
    main()
