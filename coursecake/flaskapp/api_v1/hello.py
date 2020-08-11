from flask import jsonify
from flask_restx import Namespace, Resource, fields

from ..limiter import limiter

api =  Namespace("hello", description= "Used for testing")



@api.route("/", endpoint = "hello")
class Hello(Resource):
    @api.response(200, "Success")
    def get(self):
        return jsonify({"hello": "world"})
