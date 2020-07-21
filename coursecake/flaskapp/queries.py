'''
This module handles all queries made to the database
'''
from .models import Courses, CoursesSchema
from ..scrapers.course_scraper import CourseScraper

def packageResults(results: list) -> dict:
    '''
    Uses marshmallow to make results JSON seriazable
    Puts list of results in dict
    '''
    coursesSchema = CoursesSchema(many = True)
    courseData = {"courses": coursesSchema.dump(results)}
    return courseData



def queryAllUCICourses() -> list:
    return Courses.query.all()



def handleUCILiveSearch(args: dict) -> dict:
    '''
    Gets the latest (hence live) courses by directly
    access the UCI course schedule (uses scraper)
    '''
    scraper = CourseScraper().getUciScraper()
    courses = scraper.getCourses(args)
    courseData = {"courses": list(course.__dict__ for course in courses.values())}

    return courseData



def handleUCICourseSearch(args: dict) -> list:
    '''
    Handles search based on request arguments.
    We check for each arg in order to "clean" the query and prevent
    malicious queries.
    Returns list of Courses rows
    '''

    # for arg in query where attribute = arg
    equalsArgs = dict()

    print(f"handleCourseSearch -- request args -- {args}")

    if (args.get("department") != None):
        equalsArgs["department"] = args["department"].upper()

    if (args.get("building") != None):
        equalsArgs["building"] = args["building"].upper()

    if (args.get("room") != None):
        equalsArgs["room"] = args["room"].upper()

    # apply filter for equals args first
    print(f"handleCourseSearch -- equalsArgs -- {equalsArgs}")
    query = Courses.query.filter_by(**equalsArgs)


    # add arguments for NOT LIKE
    if(args.get("notlocation") != None):
        notLocation = args.get("notlocation").upper()
        query = query.filter(~Courses.location.like(
            f"%{notLocation}%"))


    if(args.get("notinstructor") != None):
        notinstructor = args.get("notinstructor").upper()
        query = query.filter(~Courses.instructor.like(
            f"%{notinstructor}%"))


    # add arguments for LIKE
    if (args.get("instructor") != None):
        instructor = args.get("instructor").upper()
        query = query.filter(Courses.instructor.like(
            f"%{instructor}%"))

    results = query.all()

    return results
