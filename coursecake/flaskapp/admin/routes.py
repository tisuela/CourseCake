from flask import make_response,jsonify,request,Blueprint

from ..limiter import limiter
from .updates import updateAllUciCourses
from .utils import verifyAdminToken


admin_blueprint = Blueprint("admin_blueprint", __name__)

@admin_blueprint.route("/admin/update-uci", methods=["POST"])
@limiter.limit("5/minute;5/hour")
def updateAllUci():
    # result stores success/failure of update
    result = dict()
    headers = {"Content-Type": "application/json"}
    status = 400

    # verify admin
    token = request.headers.get("token")

    if (verifyAdminToken(token)):
        updateAllUciCourses()

        result["result"] = "success"

    else:
        result["result"] = "fail"
        result["reason"] = "bad_token"
        status = 401


    return make_response(
        jsonify(result),
        status,
        headers
    )
