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

    db.init_app(app)
    ma.init_app(app)

    from .routes import limiter
    limiter.init_app(app)
    # db.drop_all(app = app)
    db.create_all(app = app)

    from .routes import route_blueprint
    app.register_blueprint(route_blueprint)

    return app
