from flask import make_response,jsonify,request,Blueprint

from ..limiter import limiter
from .updates import updateAllUCICourses



admin_blueprint = Blueprint("admin_blueprint", __name__)

@admin_blueprint.route("/admin/update-uci", methods=["GET"])
@limiter.limit("5/minute;5/hour")
def updateAllUCI():
    # result stores success/failure of update
    result = dict()
    updateAllUCICourses()

    result["result"] = "success"

    headers = {"Content-Type": "application/json"}
    return make_response(
        jsonify(result),
        200,
        headers
    )
