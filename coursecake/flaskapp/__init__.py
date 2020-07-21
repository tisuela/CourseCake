'''
Runs flask app
'''
import os

from flask import Flask
from .models import db,ma




def create_app(test_config=None):
    # init app
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY = "dev",
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_DATABASE_URI = "sqlite:///../db.sqlite"
    )

    # initialize database
    db.init_app(app)

    # db.drop_all(app = app)
    db.create_all(app = app)

    # initialize database serializer
    ma.init_app(app)

    # import API rate limiter
    from .limiter import limiter

    # initialize API Rate limiter
    limiter.init_app(app)

    # import api routes
    from .api.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    # import admin routes
    from .admin.routes import admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
