from ....scrapers.course_scraper import CourseScraper

def uci_live_search_courses(args: dict, term_id: str = "FAll-2020-1") -> dict:
    '''
    Gets the latest (hence live) courses by directly
    access the Uci course schedule (uses scraper)
    '''
    term_args = term_id.split("-")

    # check if term_id is fully specified
    # if not, fill in assumed values
    if (len(term_args) < 3):
        term_id += "-1"

    scraper = CourseScraper().getUciScraper()

    scraper.set_term_id(term_id = term_id)

    courses = scraper.getCourses(args)
    courseData = list(course.__dict__ for course in courses.values())

    return courseData
