'''
Runs flask app
'''
import os

from flask import Flask
from flask import jsonify
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
    default_limits = ["30 per minute"])


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_DATABASE_URI = "sqlite:///../db.sqlite"
    )

    db.init_app(app)
    ma.init_app(app)
    # db.drop_all(app = app)
    db.create_all(app = app)



    @app.route("/hello", methods=["GET"])
    def hello():
        return jsonify({"hello": "world"})



    @app.route("/api/uci/all", methods=["GET"])
    def uciAllCourses():

        # make query results json seriazable via marshmallow
        coursesSchema = CoursesSchema(many = True)
        toJson = coursesSchema.dump(results)
        return jsonify(toJson)



    @app.route("/api/admin/update-uci", methods=["GET"])
    @limiter.limit("1/minute;5/hour")
    def updateAllUCICourses():
        # result stores success/failure of update
        result = dict()
        courseScraper = CourseScraper()
        courses = courseScraper.getAllUCICourses()

        for course in courses.values():
            newCourse = Courses(course)
            db.session.add(newCourse)

        db.session.commit()
        result["result"] = success

        return jsonify(result)








    return app






class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)




class Courses(db.Model):
    code = db.Column(db.String(20), primary_key=True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    instructor = db.Column(db.String(50), nullable = False)
    time = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(50), nullable = False)
    status = db.Column(db.String(20), nullable = False)

    units = db.Column(db.Integer, nullable = False)

    type = db.Column(db.String(20), nullable = True)



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
        self.status = course.status

        self.units = course.units

        self.type = course.type


    def __repr__(self):
        return f"{self.code} | {self.name} | {self.instructor} | {self.units} | {self.status} \n"



class CoursesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Courses
