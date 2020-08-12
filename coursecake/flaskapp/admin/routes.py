from flask import make_response,jsonify,request,Blueprint
from ..limiter import limiter
from .updates import updateAllUciCourses, reloadCoursesModel,\
                reloadUniversityModel, reloadAllModels
from .utils import verifyAdminToken, doAdminFunc


admin_blueprint = Blueprint("admin_blueprint", __name__)

@admin_blueprint.route("/admin/update-uci", methods=["POST"])
@limiter.limit("5/minute;5/hour")
def updateAllUci():

    return doAdminFunc(request, updateAllUciCourses)




@admin_blueprint.route("/admin/reload/courses", methods=["POST"])
@limiter.limit("5/minute;5/hour")
def reloadCourses():
    '''
    Drops and recreates Courses model

    Used when the model Schema is updated --
    we can remotely update it instead of having to hardcode
    a .drop() method somewhere in execution
    '''

    return doAdminFunc(request, reloadCoursesModel)


@admin_blueprint.route("/admin/reload/university", methods=["POST"])
@limiter.limit("5/minute;5/hour")
def reloadUniverity():
    '''
    Drops and recreates University model

    Used when the model Schema is updated --
    we can remotely update it instead of having to hardcode
    a .drop() method somewhere in execution
    '''

    return doAdminFunc(request, reloadUniversityModel)



@admin_blueprint.route("/admin/reload/all", methods=["POST"])
@limiter.limit("5/hour")
def reloadAll():
    '''
    Drops and recreates University model

    Used when the model Schema is updated --
    we can remotely update it instead of having to hardcode
    a .drop_all() method somewhere in execution
    '''

    return doAdminFunc(request, reloadAllModels)
