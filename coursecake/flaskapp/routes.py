
from flask import make_response,jsonify,request,Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .queries import handleUCICourseSearch,\
                        queryAllUCICourses,packageResults
from .updates import updateAllUCICourses



route_blueprint = Blueprint("route_blueprint", __name__)



# enforces rate limits for all endpoints
limiter = Limiter(
    key_func = get_remote_address,
    default_limits = ["1/second; 20/minute"])



@route_blueprint.route("/hello", methods=["GET"])
def hello():
    headers = {"Content-Type": "application/json"}
    return make_response(
        jsonify({"hello": "world"}),
        200,
        headers
    )



@route_blueprint.route("/api/uci/courses/all", methods=["GET"])
def uciAll():
    results = queryAllUCICourses()
    courseData = packageResults(results)


    headers = {"Content-Type": "application/json"}
    return make_response(
        jsonify(courseData),
        200,
        headers
    )



@route_blueprint.route("/api/uci/courses/search", methods=["GET"])
def uciSearch():
    args = request.args
    results = handleUCICourseSearch(args)
    courseData = packageResults(results)

    headers = {"Content-Type": "application/json"}
    return make_response(
        jsonify(courseData),
        200,
        headers
    )



@route_blueprint.route("/admin/update-uci", methods=["GET"])
@limiter.limit("1/minute;5/hour")
def updateAllUCI():
    # result stores success/failure of update
    result = dict()
    updateAllUCI()

    result["result"] = "success"

    headers = {"Content-Type": "application/json"}
    return make_response(
        jsonify(result),
        200,
        headers
    )
