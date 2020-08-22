# all operations to db are here
import re

from sqlalchemy.orm import Session

from . import models
from ..scrapers.course import Course


def get_universities(db: Session, offset: int = 0, limit: int = 100) -> list:
    return db.query(models.University).offset(offset).limit(limit).all()

def get_university(db: Session, name: str) -> models.University:
    return db.query(models.University).filter(models.University.name == name.upper()).first()


def add_university(db: Session, name: str) -> models.University:
    university = models.University(name=name.upper())
    db.add(university)
    db.commit()
    db.refresh(university)
    return university


def get_courses(db: Session, offset: int = 0, limit: int = 100) -> list:
    return db.query(models.Course).offset(offset).limit(limit).all()


def add_course(db: Session, university: str, courseObj: Course, commit: bool = True) -> models.Course:
    '''
    courseObj is the basic python instance of Course defined in
    scrapers.course

    courseModelis SQL version
    '''
    courseModel = models.Course(courseObj, university.upper())
    db.add(courseModel)

    if commit:
        db.commit()
        db.refresh(courseModel)
    return courseModel


def bulk_add_course(db: Session, university: str, courses: list):
    toInsert = list()
    university = university.upper()
    for courseObj in courses:
        toInsert.append(models.Course(courseObj, university))

    db.bulk_save_objects(toInsert)
    db.commit()



class CourseQuery:
    '''
    dynamically builds a query for courses and executes it
    '''
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

    def __init__(self, db: Session, university: str, args: dict):

        # {"parameter[filter]": "value1,value2,etc"}
        self.args = args
        self.query = db.query(models.University).filter(models.University.name == university.upper()).first().courses



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
