# packaging for flaskapp
import os
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from ..scraper.course_scraper import CourseScraper

# create the database
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_DATABASE_URI = "sqlite:///../db.sqlite"
    )

    db.init_app(app)
    db.create_all(app = app)




    @app.route("/hello")
    def hello():
        courseScraper = CourseScraper()
        return jsonify(courseScraper.getAllUcIrvineCourses())


    @app.route("/test")
    def testdb():
        test = Test(name = "sup")
        db.session.add(test)
        db.session.commit()
        print(Test.query.all())
        return "test success"


    return app


class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
