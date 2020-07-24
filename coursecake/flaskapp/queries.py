'''
This module handles all queries made to the database
'''
from .models import University, Courses, CoursesSchema
from ..scrapers.course_scraper import CourseScraper

def packageResults(results: list) -> dict:
    '''
    Uses marshmallow to make results JSON seriazable
    Puts list of results in dict
    '''
    coursesSchema = CoursesSchema(many = True)
    courseData = {"courses": coursesSchema.dump(results)}
    return courseData



def queryAllUciCourses() -> list:
    return University.query.filter_by(name = "UCI").first().courses



def handleUciLiveSearch(args: dict) -> dict:
    '''
    Gets the latest (hence live) courses by directly
    access the Uci course schedule (uses scraper)
    '''
    scraper = CourseScraper().getUciScraper()
    courses = scraper.getCourses(args)
    courseData = {"courses": list(course.__dict__ for course in courses.values())}

    return courseData

def checkToInt(column: str, value: str):
    '''
    tbh this feels like a terrible function
    but im gonna do it

    returns string when the column is string
    returns int when the column is int
    '''
    intColumns = ["units", "enrolled"]

    if (column in intColumns):
        return int(value)
    return value


def addInFilter(args: dict, column: str, query):
    '''
    Adds the '_in' filter for queries (for single or multiple values)
    in a column.
    Filter values in the args dict are comma separated.
    Returns Query
    '''
    if (args.get(column) != None):

        # convert all values to uppercase (values are comma separated)
        filterValues = [checkToInt(column, v.upper()) for v in args[column].split(",")]
        query = query.filter(Courses.__table__.c[column].in_(filterValues))

    return query



def addNotInFilter(args: dict, parameter: str, query):
    '''
    Adds the '~_in' filter for queries (for single or multiple values)
    in a column.
    Filter values in the args dict are comma separated.
    Returns Query
    '''
    if (args.get(parameter) != None):
        # remove "not" from parameter to get column name
        column = parameter.replace("not", "")

        # convert all values to uppercase (values are comma separated)
        filterValues = [checkToInt(column, v.upper()) for v in args[parameter].split(",")]
        query = query.filter(~Courses.__table__.c[column].in_(filterValues))

    return query



def addLikeFilter(args: dict, column: str, query):
    '''
    Adds the 'like' filter for queries (for single or multiple values)
    Filter values in the args dict are comma separated.
    Returns Query
    '''
    if (args.get(column) != None):

        for value in args[column].split(","):
             value = value.upper()
             print(f"value = {value}")
             query = query.filter(Courses.__table__.c[column].ilike(f"%{value}%"))

    return query



def addNotLikeFilter(args: dict, parameter: str, query):
    '''
    Adds the '~like' filter for queries (for single or multiple values)
    Filter values in the args dict are comma separated.
    Returns Query
    '''
    if (args.get(parameter) != None):
            # remove "not" from parameter to get column name
            column = parameter.replace("not", "")

            for value in args[parameter].split(","):
                 value = value.upper()
                 query = query.filter(~Courses.__table__.c[column].like(f"%{value}%"))

    return query




def handleUciCourseSearch(args: dict) -> list:
    '''
    Handles search based on request arguments.
    We check for each arg in order to "clean" the query and prevent
    malicious queries.
    Returns list of Courses rows
    '''

    query = Courses.query
    print(f"handleCourseSearch -- request args -- {args}")

    query = addInFilter(args, "code", query)
    query = addInFilter(args, "department", query)
    query = addInFilter(args, "buidling", query)
    query = addInFilter(args, "room", query)
    query = addInFilter(args, "status", query)
    query = addInFilter(args, "units", query)

    query = addNotInFilter(args, "notinstructor", query)
    query = addNotInFilter(args, "notbuilding", query)
    query = addNotInFilter(args, "notroom", query)
    query = addNotInFilter(args, "notunits", query)

    query = addLikeFilter(args, "instructor", query)
    query = addLikeFilter(args, "name", query)
    query = addLikeFilter(args, "title", query)
    query = addLikeFilter(args, "time", query)
    query = addLikeFilter(args, "location", query)

    query = addNotLikeFilter(args, "nottime", query)
    query = addNotLikeFilter(args, "notlocation", query)

    results = query.all()

    return results
