from .ucirvine_scraper import UCIrvineScraper
from .course import Course

import json

class CourseScraper:
    def __init__(self):
        pass

    def downloadUCIrvineCourses(self):
        courses = UCIrvineScraper().scrape()
        self.downloadCoursesAsJson(courses, "UCIrvineCourses.json")


    def downloadCoursesAsJson(self, courses, fileName):
        with open(fileName, "w+") as jsonFile:
            json.dump({"courses": list(course.__dict__ for course in courses)}, jsonFile)


        jsonFile.close()


    def getAllUcIrvineCourses(self) -> str:
        courses = UCIrvineScraper().getDepartmentCourses("COMPSCI")
        return {"courses": list(course.__dict__ for course in courses)}






def main():
    courseScraper = CourseScraper()

    course = Course()
    course.name = "yeet"
    course.code = "1223"
    courses = [course]

    courseScraper.downloadUCIrvineCourses()
    # courseScraper.downloadCoursesAsJson(courses, "test.json")



if __name__ == '__main__':
    main()
