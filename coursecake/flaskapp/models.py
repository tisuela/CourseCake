'''
Holds all models for SQLAlchemy and marshmallow
'''
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


# create the database
db = SQLAlchemy()
ma = Marshmallow()

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)


class Courses(db.Model):
    '''
    This table is very detailed, getting all information we can possibly
    collect about a Course. It may be better practice to separate it to
    multiple tables, but we are not worried about database size right now.
    We want all course information to be easily accessed from one model
    without having to join multiple tables

    To compensate, other tables will be made (like University) whose
    information is redundant but will aid in query performance.
    '''

    # The university where this course is offered
    # This should be the university's domain name in all CAPS
    # Ex: UC Irvine's domain is uci.edu, so university = UCI
    university = db.Column(db.String(20), db.ForeignKey("university.name"), primary_key=True,  nullable = False)

    # Course code which is unique to the univerisity
    # It is not necessarily unique to the database,
    # Which is why university + code are primary keys
    code = db.Column(db.String(20), primary_key=True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    department = db.Column(db.String(50), nullable = False)
    instructor = db.Column(db.String(50), nullable = False)
    time = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(50), nullable = False)
    building = db.Column(db.String(50), nullable = False)
    room = db.Column(db.String(50), nullable = False)
    status = db.Column(db.String(20), nullable = False)
    type = db.Column(db.String(20), nullable = False)

    units = db.Column(db.Integer, nullable = False)
    max = db.Column(db.Integer, nullable = False)
    enrolled = db.Column(db.Integer, nullable = False)
    waitlisted = db.Column(db.Integer, nullable = False)
    requested = db.Column(db.Integer, nullable = False)

    # nullable fields

    departmentTitle = db.Column(db.String(50), nullable = False)
    restrictions = db.Column(db.String(100), nullable = False)
    school = db.Column(db.String(50), nullable = False)

    updated = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    prerequisites = db.relationship("Prerequisite", backref = "courses", lazy="dynamic")


    def __init__(self, course, university: str):
        '''
        Courses uses a course objects
        See ../scraper/course.py
        '''
        self.university = university
        self.code = course.code
        self.name = course.name
        self.title = course.title
        self.department = course.department
        self.instructor = course.instructor
        self.time = course.time
        self.location = course.location
        self.building = course.building
        self.room = course.room
        self.status = course.status
        self.type = course.type

        self.units = course.units
        self.max = course.max
        self.enrolled = course.enrolled
        self.waitlisted = course.waitlisted
        self.requested = course.requested

        self.departmentTitle = course.departmentTitle
        self.restrictions = course.restrictions
        self.school = course.school



    def __repr__(self):
        return f"{self.code} | {self.name} | {self.instructor} | {self.units} | {self.status} \n"


class University(db.Model):
    '''
    Holds redundant information, but might?? aid in future queries
    or refactors
    '''

    # The university where this course is offered
    # This should be the university's domain name in all CAPS
    # Ex: UC Irvine's domain is uci.edu, so university = UCI
    name = db.Column(db.String(20), primary_key=True, nullable = False)
    courses = db.relationship("Courses", backref = "thisUniversity", lazy="dynamic")


    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"{self.name}"






class Prerequisite(db.Model):
    '''
    Stores a prerequisite to a course
    '''
    thisCode = db.Column(db.String(20), db.ForeignKey("courses.code"), primary_key=True,  nullable = False)
    prerequisiteCode = db.Column(db.String(20), primary_key=True, nullable = False)



class CoursesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Courses
