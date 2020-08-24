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
    # client.post("/api/v1/admin/update/all?token=zot")
    uploads.update_all(db)

    response = client.get("/api/v1/courses/all")
    assert response.status_code == 200


def test_basic_search():
    response = client.get("/api/v1/courses/search/uci")
    assert response.status_code == 200


def test_medium_search():
    response = client.get("/api/v1/courses/search/uci?department=compsci")
    assert response.status_code == 200



def test_basic_live_search():
    response = client.get("/api/v1/courses/live-search/uci?department=compsci")
    assert response.status_code == 200
