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
    @api.response(200, "Success", model = coursesModel)
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
                "description": "Unique department code (Check your Uni's website)"
            },
            "location": {
                "in": "query",
                "description": "Includes building and room info"
            },
            "building": {
                "in": "query",
                "description": "Building name where instruction occurs"
            },
            "room": {
                "in": "query",
                "description": "Room name/number where instruction occurs"
            },
            "status": {
                "in": "query",
                "description": "Status of class enrollment (FULL, OPEN, CLOSED, etc.)"
            },
            "units": {
                "in": "query"
            },
            "enrolled":{
                "in": "query",
                "description": "Number of students currently enrolled in the course"
            },
            "waitlisted": {
                "in": "query"
            },
            "requested": {
                "in": "query"
            },
            "max": {
                "in": "query",
                "description": "Maximum number of students that can be enrolled"
            },
            "instructor": {
                "in": "query",
                "description": "Instructor(s) teaching the course"
            },
            "time": {
                "in": "query",
                "description": "Time of instruction throughout the week. Ex: MWF 10am-11am"
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



@api.route("/live-search/<string:university>", endpoint = "live-search")
@api.doc(params={"university": "Based on their domain.edu"})
class LiveSearch(Resource):
    @api.response(200, "Success",model = coursesModel)
    @api.doc(params = {
            "code": {
                "in": "query",
                "description": "Unique course code"
                },
            "title": {
                "in": "query",
                "description": "More readable name of the course"
            },

            "department": {
                "in": "query",
                "description": "Unique department code (Check your Uni's website)"
            },
            "units": {
                "in": "query"
            },
            "instructor": {
                "in": "query",
                "description": "Instructor(s) teaching the course"
            },
            "breadth": {
                "in": "query",
                "description": "GE requirement of the course. Ex: GE-2"
            },
            "starttime": {
                "in": "query",
                "description": "Course must begin daily instruction after this time. Ex: 8:00am"
            },
            "endtime": {
                "in": "query",
                "description": "Course must end daily instruction after this time. Ex: 9:30pm"
            }
    })
    def get(self, university: str):
        '''
        Searches for courses based on the latest data (by accessing the course schedule directly).
        Because it is live, this resource is ratelimited and making complex queries is not possible.

        You MUST specify AT LEAST ONE of the following parameters:
        `code`, `department`, `instructor`, or `breadth`
        '''
        current_app.logger.info("live search requested")
        try:
            args = request.args
            courseData = dict()
            if (university.lower() == "uci"):
                courseData = handleUciLiveSearch(args)

            return jsonify(courseData)

        except:
            return jsonify({"errorMessage": "bad args"})
