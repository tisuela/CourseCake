import time
import pytest

from fastapi.testclient import TestClient

from ...database import crud, models, uploads
from ...database.sql import SessionLocal, engine
from ..main import app

client = TestClient(app)




@pytest.fixture(scope="module")
def db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    models.Base.metadata.drop_all(bind=engine)


def test_all(db):
    # need to populate db first
    uploads.update_all(db, testing = True)

    response = client.get("/api/v1/courses/all")
    assert response.status_code == 200
    assert len(response.json()) >= 50


def test_basic_search():
    response = client.get("/api/v1/courses/search/uci")
    assert response.status_code == 200
    assert len(response.json()) >= 50


def test_medium_search():
    response = client.get("/api/v1/courses/search/uci?department=art")
    assert response.status_code == 200
    assert len(response.json()) >= 10


def test_heavy_search():
    response = client.get("/api/v1/courses/search/uci?department[like]=co&professor[ilike]=pattis&units[not]=8")
    assert response.status_code == 200
    assert len(response.json()) >= 5


def atest_basic_live_search():
    response = client.get("/api/v1/courses/live-search/uci?department=compsci&badarg=harmful")
    assert response.status_code == 200
    assert len(response.json()) >= 50


def test_upload_all():
    response = client.post("/api/v1/admin/update/all?token=bad")
    assert response.status_code == 401
