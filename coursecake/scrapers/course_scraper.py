from .uci.uci_scraper import UciScraper
from .ucsc.ucsc_scraper import UcscScraper
from .course import Course
from .scraper import Scraper
import json

class CourseScraper:
    '''
    All courses can be scraped from here
    '''
    REGISTERED_SCRAPERS = {
        "UCI": UciScraper,
        "UCSC": UcscScraper
    }

    def __init__(self):

        # Useful to construct other courses using the existing populated
        # attributes from this template
        # Ex: newCourse = Course(self.templateCourse.__dict__)
        self.templateCourse = Course()

    def get_scraper(self, university: str, term_id: str = "2020-FALL-1") -> Scraper:
        university = university.upper()

        return self.REGISTERED_SCRAPERS[university](term_id)


    def getUciScraper(self) -> UciScraper:
        return UciScraper()

    def getAllUciCourses(self) -> dict:
        courses = UciScraper().scrape()

        # courses = UciScraper().getDepartmentCourses("COMPSCI")
        return courses


    def downloadCoursesAsJson(self, courses, fileName):
        with open(fileName, "w+") as jsonFile:
            json.dump({"courses": list(course.__dict__ for course in courses.values())}, jsonFile)


        jsonFile.close()






'''
only used for testing
def main():
    courseScraper = CourseScraper()


    scraper = courseScraper.getUciScraper()

    args = dict()
    while (True):
        searchParam = input("search parameter: ")
        if (searchParam.strip().lower() == "d"):
            break
        searchValue = input("search value: ")
        args[searchParam] = searchValue

    courses = scraper.getCourses(args)

    for course in courses.values():
        print(course)
    # courseScraper.downloadCoursesAsJson(courses, "test.json")
    print(f"# of results = {len(courses)}")


if __name__ == '__main__':
    main()
'''
