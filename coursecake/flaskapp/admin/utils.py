from flask import make_response,jsonify

from ...config import Config


def verifyAdminToken(token: str) -> bool:
    return token == Config.ADMIN_TOKEN




def doAdminFunc(request, func, *args):
    '''
    Automates admin checks and response creation
    '''
    # result stores success/failure of update
    result = dict()
    headers = {"Content-Type": "application/json"}
    status = 400

    # verify admin
    token = request.headers.get("token")

    if (verifyAdminToken(token)):
        func(*args)

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
