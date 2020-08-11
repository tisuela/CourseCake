import json
from flask import make_response,jsonify,request,Blueprint,current_app
from flask_restx import Namespace, Resource, fields
from marshmallow_jsonschema import JSONSchema

from ..limiter import limiter
from ..queries import CourseSearch,handleUciLiveSearch,\
                        queryAllCourses,packageResults
from ..models import CoursesSchema

api =  Namespace("courses", description= "Search for courses")


# get courses model for documentation (via flask-restx via SwaggerUI)
coursesSchema = CoursesSchema()
jsonSchema = JSONSchema()
coursesModel = api.schema_model("Course", jsonSchema.dump(coursesSchema)["definitions"]["CoursesSchema"])

@api.route("/all/<string:university>", endpoint = "all")
class AllCourses(Resource):
    @api.response(200, "Success")
    def get(self, university: str):
        current_app.logger.info("all courses requested")
        results = queryAllCourses(university.upper())
        courseData = packageResults(results)

        return jsonify(courseData)


@api.route("/search/<string:university>", endpoint = "search")
@api.doc(params={"university": "Based on their domain.edu"})
class Search(Resource):
    @api.response(200, "Success",model = coursesModel)
    @api.doc(params = {
            "code": {
                "in": "query",
                "description": "Unique course code"
                },

            "name": {
                "in": "query",
                "description": "Formal name of the course"
            },

            "title": {
                "in": "query",
                "description": "More readable name of the course"
            },

            "department": {
                "in": "query",
                "description": "Unique department code"
                }
    })
    def get(self, university: str):
        '''
        Returns list of courses matching query

        # Filters - Make Powerful Queries
        All parameter names can be followed be [filter].
        The default filter (applied when no filter is specified) is `equals`

        For example:
        ```title[like]=dance```

        Here are all valid filters:
        `like`
        `notlike`
        `equals`
        `notequals`

        # Search for multiple values
        You can add multiple values for each parameter delimited by commas `,`.

        For example:
        ```units=4,2,1```

        This also works with filters:
        ```building[like]=pavlilion,lounge,plaza&building[not]=library,hall```

        '''
        current_app.logger.info("course search requested")
        args = request.args
        search = CourseSearch(university.upper(), args)
        results = search.search()
        courseData = packageResults(results)

        headers = {"Content-Type": "application/json"}
        return jsonify(courseData)
