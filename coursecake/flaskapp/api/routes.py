
from flask import make_response,jsonify,request,Blueprint

from ..limiter import limiter
from ..queries import handleUciCourseSearch,handleUciLiveSearch,\
                        queryAllUciCourses,packageResults




api_blueprint = Blueprint("api_blueprint", __name__)





@api_blueprint.route("/api/hello", methods=["GET"])
def hello():
    headers = {"Content-Type": "application/json"}
    return make_response(
        jsonify({"hello": "world"}),
        200,
        headers
    )



@api_blueprint.route("/api/uci/courses/all", methods=["GET"])
def UciAll():
    results = queryAllUciCourses()
    courseData = packageResults(results)


    headers = {"Content-Type": "application/json"}
    return make_response(
        jsonify(courseData),
        200,
        headers
    )



@api_blueprint.route("/api/uci/courses/search", methods=["GET"])
def UciSearch():
    args = request.args
    results = handleUciCourseSearch(args)
    courseData = packageResults(results)

    headers = {"Content-Type": "application/json"}
    return make_response(
        jsonify(courseData),
        200,
        headers
    )


@api_blueprint.route("/api/uci/courses/live-search", methods=["GET"])
@limiter.limit("5/minute;60/hour")
def UciLiveSearch():
    try:
        args = request.args
        courseData = handleUciLiveSearch(args)

        headers = {"Content-Type": "application/json"}
        return make_response(
            jsonify(courseData),
            200,
            headers
        )
    except:
        headers = {"Content-Type": "application/json"}
        return make_response(
            jsonify({"errorMessage": "bad args"}),
            400,
            headers
        )
