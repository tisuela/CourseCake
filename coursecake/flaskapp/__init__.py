# packaging for flaskapp
import os
from flask import Flask
from flask import jsonify

from ..scraper.course_scraper import CourseScraper
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = "dev"
    )



    @app.route("/hello")
    def hello():
        courseScraper = CourseScraper()
        return jsonify(courseScraper.getAllUcIrvineCourses())


    return app
