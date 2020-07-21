'''
Modify this file or your environmental vars for production deployment
'''
import os


class Config:
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///../db.sqlite"

    if (os.environ.get("SECRET_KEY") != None):
        SECRET_KEY = os.environ.get("SECRET_KEY")

    if (os.environ.get("SQLALCHEMY_DATABASE_URI ") != None):
        SQLALCHEMY_DATABASE_URI  = os.environ.get("SQLALCHEMY_DATABASE_URI ")
