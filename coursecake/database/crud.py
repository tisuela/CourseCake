# all operations to db are here
import re

from sqlalchemy.orm import Session

from . import models
from ..scrapers.course import Course
from ..scrapers.course_class import CourseClass

def get_universities(db: Session, offset: int = 0, limit: int = 100) -> list:
    return db.query(models.University).offset(offset).limit(limit).all()

def get_university(db: Session, name: str) -> models.University:
    return db.query(models.University).filter(models.University.name == name.upper()).first()


def add_university(db: Session, name: str) -> models.University:
    university = models.University(name=name.upper())
    db.merge(university)
    db.commit()
    return university


def get_courses(db: Session, offset: int = 0, limit: int = 100) -> list:
    return db.query(models.Course).offset(offset).limit(limit).all()


def add_course(db: Session, university: str, term: str, courseObj: Course, commit: bool = True) -> models.Course:
    '''
    courseObj is the basic python instance of Course defined in
    scrapers.course

    courseModelis SQL version
    '''
    courseModel = models.Course(courseObj, university.upper(), term.upper())
    db.merge(courseModel)

    if commit:
        db.commit()
    return courseModel


def add_class(db: Session, university: str, term: str, classObj: CourseClass, commit: bool = True) -> models.Course:
    '''
    classeObj is the basic python instance of CourseClass defined in
    scrapers.course_class

    classModel is SQL version
    '''
    classModel = models.Class(classObj, university.upper(), term.upper())
    db.merge(classModel)

    if commit:
        db.commit()
    return classModel


def bulk_add_courses(db: Session, university: str, term: str, courses: list):
    '''
    DOES NOT MERGE
    '''
    toInsert = list()
    university = university.upper()
    term = term.upper()
    for courseObj in courses:
        toInsert.append(models.Course(courseObj, university, term))

    db.bulk_save_objects(toInsert)
    db.commit()




def bulk_merge_courses(db: Session, university: str, term: str, courses: list):

    for course in courses:
        if course.is_valid_course():
            add_course(db, university.upper(), term.upper(), course, commit = False)
        else:
            # print("INVALID COURSE", course)
            pass
    db.commit()


def bulk_merge_classes(db: Session, university: str, term: str, classes: list):

    for a_class in classes:
        add_class(db, university.upper(), term.upper(), a_class, commit = False)

    db.commit()


class CourseQuery:
    '''
    dynamically builds a query for courses and executes it
    '''
    QUERY_DELIMITER = ","
    CURRENT_TERM_ID = "2020-FALL-1"

    # these constants help clean the query from malicious requests
    # TODO: Fix departmentTitle
    VALID_PARAMETERS = [
        "id",
        "title",
        "department",
        "units"
    ]

    VALID_FILTERS = [
        "like",
        "equals",
        "not",
        "notlike"
    ]

    CASE_SENSITIVE_PARAMETERS = [
        "id"
    ]

    def __init__(self, db: Session, university: str, args: dict = dict(), term_id: str = CURRENT_TERM_ID, offset: int = 0, limit: int = 500):
        university = university.upper()
        term_id = term_id.upper()

        # {"parameter[filter]": "value1,value2,etc"}
        self.args = args

        self.offset = offset
        self.limit = limit

        if term_id != None:
            term_args = term_id.split("-")

            # check if term_id is fully specified
            # if not, fill in assumed values
            if (len(term_args) < 3):
                term_id += "-1"

            # print(f"searching {university} for max of {limit} results")

            self.query = db.query(models.University).filter(models.University.name == university).first().courses.filter(models.Course.term_id == term_id)
        else:
            self.query = db.query(models.University).filter(models.University.name == university).first().courses




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
            self.query = self.query.filter(models.Course.__table__.c[column].ilike(f"%{value}%"))



    def _addNotLikeFilter(self, column: str, filter: str, values: list):
        '''
        Adds LIKE filter to query
        '''
        for value in values:
            value = value.upper()
            self.query = self.query.filter(~models.Course.__table__.c[column].ilike(f"%{value}%"))



    def _addEqualsFilter(self, column: str, filter: str, values: list):
        '''
        Adds EQUALS filter to query
        '''
        self.query = self.query.filter(models.Course.__table__.c[column].in_(values))



    def _addNotEqualsFilter(self, column: str, filter: str, values: list):
        '''
        Adds NOT EQUALS filter to query
        '''
        self.query = self.query.filter(~models.Course.__table__.c[column].in_(values))



    def _buildQuery(self):
        # within args, a query is defined as:
        # {"parameter[filter]": "value1,value2,etc"}
        # We parse over the keys and values of args to build the query
        for arg in self.args:
            # parameter is defined before filter
            parameter = arg.split("[")[0].lower()

            # clean query
            if (parameter in self.VALID_PARAMETERS):
                if parameter in self.CASE_SENSITIVE_PARAMETERS:
                    queryValues = [self.checkToInt(parameter, v) for v in self.args[arg].split(self.QUERY_DELIMITER)]
                else:
                    queryValues = [self.checkToInt(parameter, v.upper()) for v in self.args[arg].split(self.QUERY_DELIMITER)]

                # filter is defined between brackets; [filter]
                filter = ""

                try:
                    filter = re.search(r"\[([A-Za-z0-9_]+)\]", arg).group(1).lower()
                except AttributeError:
                    # catch error when no filter is specified
                    # when no filter is specified, filter is assumed to be equals; "="
                    pass

                # add filters
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
        results = self.query.offset(self.offset).limit(self.limit).all()

        return results


class ClassQuery:
    '''
    dynamically builds a query for courses and executes it
    '''
    QUERY_DELIMITER = ","
    CURRENT_TERM_ID = "2020-FALL-1"

    # these constants help clean the query from malicious requests
    # TODO: Fix departmentTitle
    VALID_PARAMETERS = [
        "id",
        "course_id",
        "location",
        "building",
        "room",
        "status",
        "instructor",
        "time",
        "units",
        "enrolled",
        "waitlisted",
        "requested",
        "max"
    ]

    VALID_FILTERS = [
        "like",
        "equals",
        "not",
        "notlike"
    ]

    CASE_SENSITIVE_PARAMETERS = [
        "id"
    ]

    def __init__(self, db: Session, university: str, args: dict = dict(), term_id: str = CURRENT_TERM_ID, offset: int = 0, limit: int = 500):
        university = university.upper()
        term_id = term_id.upper()

        # {"parameter[filter]": "value1,value2,etc"}
        self.args = args

        self.offset = offset
        self.limit = limit

        if term_id != None:
            term_args = term_id.split("-")

            # check if term_id is fully specified
            # if not, fill in assumed values
            if (len(term_args) < 3):
                term_id += "-1"

            # print(f"searching {university} for max of {limit} results")

            self.query = db.query(models.University).filter(models.University.name == university).first().classes.filter(models.Course.term_id == term_id)
        else:
            self.query = db.query(models.University).filter(models.University.name == university).first().classes




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
            self.query = self.query.filter(models.Class.__table__.c[column].ilike(f"%{value}%"))



    def _addNotLikeFilter(self, column: str, filter: str, values: list):
        '''
        Adds LIKE filter to query
        '''
        for value in values:
            value = value.upper()
            self.query = self.query.filter(~models.Class.__table__.c[column].ilike(f"%{value}%"))



    def _addEqualsFilter(self, column: str, filter: str, values: list):
        '''
        Adds EQUALS filter to query
        '''
        self.query = self.query.filter(models.Class.__table__.c[column].in_(values))



    def _addNotEqualsFilter(self, column: str, filter: str, values: list):
        '''
        Adds NOT EQUALS filter to query
        '''
        self.query = self.query.filter(~models.Class.__table__.c[column].in_(values))



    def _buildQuery(self):
        # within args, a query is defined as:
        # {"parameter[filter]": "value1,value2,etc"}
        # We parse over the keys and values of args to build the query
        for arg in self.args:
            # parameter is defined before filter
            parameter = arg.split("[")[0].lower()

            # clean query
            if (parameter in self.VALID_PARAMETERS):
                if parameter in self.CASE_SENSITIVE_PARAMETERS:
                    queryValues = [self.checkToInt(parameter, v) for v in self.args[arg].split(self.QUERY_DELIMITER)]
                else:
                    queryValues = [self.checkToInt(parameter, v.upper()) for v in self.args[arg].split(self.QUERY_DELIMITER)]

                # filter is defined between brackets; [filter]
                filter = ""

                try:
                    filter = re.search(r"\[([A-Za-z0-9_]+)\]", arg).group(1).lower()
                except AttributeError:
                    # catch error when no filter is specified
                    # when no filter is specified, filter is assumed to be equals; "="
                    pass

                # add filters
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
        results = self.query.offset(self.offset).limit(self.limit).all()

        return results
