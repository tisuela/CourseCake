import pytest
import os
import collections

from coursecake.flaskapp import create_app
from coursecake.flaskapp import db
from coursecake.flaskapp.admin import updates



@pytest.fixture
def client():
    app = create_app({"TESTING": True})

    context = app.app_context()
    context.push()

    with app.test_client() as client:
        yield client


    context.pop()


def testHome(client):
    response = client.get("/")
    assert response.status_code == 200



def testHello(client):
    response = client.get("/api/v1/hello/")
    assert response.status_code == 200
    assert response.json["hello"] == "world"


def testReloadDb(client):
    '''
    Would test routes, but admin token is subject to change
    '''
    updates.reloadAllModels()
    courses = updates.updateAllUciCourses()

    assert len(courses) > 100


def testCoursesSearch(client):
    university = "uci"
    headers = {"department": "compsci"}
    response = client.get(f"/api/v1/courses/search/{university}", headers=headers)

    assert response.status_code == 200
    assert len(response.json["courses"]) > 10


def testCoursesAll(client):
    university = "uci"
    response = client.get(f"/api/v1/courses/all/{university}")

    assert response.status_code == 200
    assert len(response.json["courses"]) > 100



def testCoursesLiveSearch(client):
    university = "uci"
    headers = {"department": "compsci"}
    response = client.get(f"/api/v1/courses/live-search/{university}", headers={"department": "compsci"})

    assert response.status_code == 200
    # assert len(response.json["courses"]) > 10
