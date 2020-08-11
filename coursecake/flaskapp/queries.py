'''
This module handles all queries made to the database
'''
import re

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



def queryAllCourses(university: str) -> list:
    return University.query.filter_by(name = university).first().courses



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




def handleCourseSearch(university: str, args: dict) -> list:
    '''
    Handles search based on request arguments.
    We check for each arg in order to "clean" the query and prevent
    malicious queries.
    Returns list of Courses rows
    '''

    query = University.query.filter_by(name = university).first().courses
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


class CourseSearch:
    QUERY_DELIMITER = ","

    # these constants help clean the query from malicious requests
    # TODO: Fix departmentTitle
    VALID_PARAMETERS = [
        "code",
        "name",
        "title",
        "department",
        "departmentTitle"
        "location",
        "building",
        "room",
        "status",
        "units",
        "enrolled",
        "waitlisted",
        "requested",
        "max",
        "instructor",
        "time"
    ]

    VALID_FILTERS = [
        "like",
        "equals",
        "not",
        "notlike"
    ]

    def __init__(self, university: str, args: dict):

        self.args = args
        self.query = University.query.filter_by(name = university).first().courses



    def checkToInt(self, column: str, value: str):
        '''
        tbh this feels like a terrible function
        but im gonna do it

        returns string when the column is string
        returns int when the column is int
        '''
        intColumns = ["units", "enrolled",
                    "requested", "waitlisted",
                    "max"]

        if (column in intColumns):
            return int(value)
        return value



    def _addLikeFilter(self, column: str, filter: str, values: list):
        '''
        Adds LIKE filter to query
        '''
        for value in values:
            value = value.upper()
            self.query = self.query.filter(Courses.__table__.c[column].ilike(f"%{value}%"))



    def _addNotLikeFilter(self, column: str, filter: str, values: list):
        '''
        Adds LIKE filter to query
        '''
        for value in values:
            value = value.upper()
            self.query = self.query.filter(~Courses.__table__.c[column].ilike(f"%{value}%"))



    def _addEqualsFilter(self, column: str, filter: str, values: list):
        '''
        Adds EQUALS filter to query
        '''
        self.query = self.query.filter(Courses.__table__.c[column].in_(values))



    def _addNotEqualsFilter(self, column: str, filter: str, values: list):
        '''
        Adds NOT EQUALS filter to query
        '''
        self.query = self.query.filter(~Courses.__table__.c[column].in_(values))



    def _buildQuery(self):
        # within args, a query is defined as:
        # {"parameter[filter]": "value1,value2,etc"}
        # We parse over the keys and values of args to build the query
        for arg in self.args:
            # parameter is defined before filter
            parameter = arg.split("[")[0].lower()

            queryValues = [self.checkToInt(parameter, v.upper()) for v in self.args[arg].split(self.QUERY_DELIMITER)]

            # filter is defined between brackets; [filter]
            filter = ""

            try:
                filter = re.search(r"\[([A-Za-z0-9_]+)\]", arg).group(1).lower()
            except AttributeError:
                # catch error when no filter is specified
                # when no filter is specified, filter is assumed to be equals; "="
                pass


            # clean query
            if (parameter in self.VALID_PARAMETERS):

                # add filters
                print(f"filter = {filter}")
                if (filter == "like"):
                    self._addLikeFilter(parameter, filter, queryValues)

                elif (filter == "notlike"):
                    self._addNotLikeFilter(parameter, filter, queryValues)

                elif (filter == "not"):
                    self._addNotEqualsFilter(parameter, filter, queryValues)

                elif (filter == "equals" or filter == ""):
                    self._addEqualsFilter(parameter, filter, queryValues)



    def search(self):
        self._buildQuery()
        results = self.query.all()

        return results
