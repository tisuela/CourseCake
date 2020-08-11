from flask import make_response,jsonify,request,Blueprint,current_app
from flask_restx import Namespace, Resource, fields

from ..limiter import limiter
from ..queries import CourseSearch,handleUciLiveSearch,\
                        queryAllCourses,packageResults

api =  Namespace("courses", description= "Search for courses")




@api.route("/all/<string:university>", endpoint = "all")
class AllCourses(Resource):
    @api.response(200, "Success")
    def get(self, university: str):
        current_app.logger.info("all courses requested")
        results = queryAllCourses(university.upper())
        courseData = packageResults(results)

        return jsonify(courseData)


@api.route("/search/<string:university>", endpoint = "search")
@api.doc(params={"university": "A Univeristy, based on their domain.edu"})
class Search(Resource):
    @api.response(200, "Success")
    @api.doc(params = {
            "code": {
                "in": "query",
                "description": "Unique course code"},
            "department": {
                "in": "query",
                "description": "Unique department code"}
    })
    def get(self, university: str):
        current_app.logger.info("course search requested")
        args = request.args
        search = CourseSearch(university.upper(), args)
        results = search.search()
        courseData = packageResults(results)

        headers = {"Content-Type": "application/json"}
        return jsonify(courseData)
