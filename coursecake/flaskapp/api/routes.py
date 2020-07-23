from flask import make_response,jsonify,request,Blueprint,current_app
import markdown
import markdown.extensions.fenced_code

from ..limiter import limiter
from ..queries import handleUciCourseSearch,handleUciLiveSearch,\
                        queryAllUciCourses,packageResults


api_blueprint = Blueprint("api_blueprint", __name__)


@api_blueprint.route("/api")
def apiPage():
    readMe = open("docs/RESTful-API.md", "r")
    mdTemplateStr = markdown.markdown(
        readMe.read(),
        extensions = ["fenced_code"]
    )

    return mdTemplateStr


@api_blueprint.route("/api/hello", methods=["GET"])
def hello():
    headers = {"Content-Type": "application/json"}
    current_app.logger.info("hello requested")
    return make_response(
        jsonify({"hello": "world"}),
        200,
        headers
    )



@api_blueprint.route("/api/uci/courses/all", methods=["GET"])
def UciAll():
    current_app.logger.info("all courses requested")
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
    current_app.logger.info("course search requested")
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
    current_app.logger.info("live search requested")
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
