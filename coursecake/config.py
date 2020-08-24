'''
Modify this file or your environmental vars for production deployment
'''
import os


class Config:
    SECRET_KEY =  os.environ.get("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///../db.sqlite")
    COURSES_DATABASE_URL = os.environ.get("COURSES_DATABASE_URL", "sqlite:///../courses.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "zot")
