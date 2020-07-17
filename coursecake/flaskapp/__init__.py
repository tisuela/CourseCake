'''
Runs flask app
'''
import os

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from ..scrapers.course_scraper import CourseScraper

# create the database
db = SQLAlchemy()
ma = Marshmallow()
limiter = Limiter(
    key_func = get_remote_address,
    default_limits = ["1/second; 20/minute"])


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_DATABASE_URI = "sqlite:///../db.sqlite"
    )

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    # db.drop_all(app = app)
    db.create_all(app = app)



    @app.route("/hello", methods=["GET"])
    def hello():
        headers = {"Content-Type": "application/json"}
        return make_response(
            jsonify({"hello": "world"}),
            200,
            headers
        )



    @app.route("/api/uci/courses/all", methods=["GET"])
    def uciAll():

        # make query results json seriazable via marshmallow
        results = Courses.query.all()
        coursesSchema = CoursesSchema(many = True)
        courseData = {"courses": coursesSchema.dump(results)}

        headers = {"Content-Type": "application/json"}
        return make_response(
            jsonify(courseData),
            200,
            headers
        )



    @app.route("/api/uci/courses/search", methods=["GET"])
    def uciSearch():
        args = request.args
        results = handleCourseSearch(args)
        coursesSchema = CoursesSchema(many = True)
        courseData = {"courses": coursesSchema.dump(results)}

        headers = {"Content-Type": "application/json"}
        return make_response(
            jsonify(courseData),
            200,
            headers
        )



    @app.route("/admin/update-uci", methods=["GET"])
    @limiter.limit("1/minute;5/hour")
    def updateAllUCICourses():
        # result stores success/failure of update
        result = dict()
        courseScraper = CourseScraper()
        courses = courseScraper.getAllUCICourses()

        for course in courses.values():
            newCourse = Courses(course)
            db.session.merge(newCourse)

        db.session.commit()
        result["result"] = "success"

        headers = {"Content-Type": "application/json"}
        return make_response(
            jsonify(result),
            200,
            headers
        )



    return app




def handleCourseSearch(args: dict) -> list:
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
