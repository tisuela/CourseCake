'''
Runs flask app
'''
import os
import logging

from flask import Flask
import flask_monitoringdashboard as dashboard
from .models import db,ma
from ..config import Config


logging.basicConfig(filename="flaskapp.log",level=logging.DEBUG)
def create_app(test_config=None):
    # init app
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_object(Config)

    if (test_config == None):
        # bind monitoring if not testing
        dashboard.config.init_from(envvar='FLASK_MONITORING_DASHBOARD_CONFIG')
        dashboard.bind(app)
    else:
        # set up testing
        pass


    # initialize database
    db.init_app(app)

    # create database tables
    db.create_all(app = app)

    # initialize database serializer
    ma.init_app(app)

    # import API rate limiter
    from .limiter import limiter

    # initialize API Rate limiter
    limiter.init_app(app)


    ### Importing routes ###

    # import home pages routes
    from .home.routes import home_blueprint
    app.register_blueprint(home_blueprint)

    # import api routes - differemt structure from other routes!

    # deprecated api
    from .api.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    # new api using flask-restx
    from .api_v1 import blueprint as api1
    app.register_blueprint(api1)

    # import admin routes
    from .admin.routes import admin_blueprint
    app.register_blueprint(admin_blueprint)

    # import error handlers
    from .errors.handlers import errors
    app.register_blueprint(errors)



    return app
