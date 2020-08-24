import pytest
from .. import crud, models, uploads
from ..sql import SessionLocal, engine


@pytest.fixture(scope="module")
def db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    models.Base.metadata.drop_all(bind=engine)


def test_update_all(db):
    uploads.update_all(db, testing = True)
    courses = crud.get_courses(db)

    assert len(courses) >= 10
