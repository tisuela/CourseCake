
from flask import Blueprint
import markdown
import markdown.extensions.fenced_code

from ..limiter import limiter

home_blueprint = Blueprint("home_blueprint", __name__)


@home_blueprint.route("/")
@home_blueprint.route("/index")
@home_blueprint.route("/readme")
def homePage():
    readMe = open("docs/README.md", "r")
    mdTemplateStr = markdown.markdown(
        readMe.read(),
        extensions = ["fenced_code"]
    )

    return mdTemplateStr
