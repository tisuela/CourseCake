'''
Holds all models for SQLAlchemy and marshmallow
'''
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




    def __init__(self, course):
        '''
        Courses uses a course objects
        See ../scraper/course.py
        '''
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



class CoursesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Courses
