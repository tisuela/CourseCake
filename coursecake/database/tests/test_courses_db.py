import pytest
from sqlalchemy.orm import Session

from .. import crud, models
from ..sql import SessionLocal, engine




@pytest.fixture(scope="module")
def db():
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    models.Base.metadata.drop_all(bind=engine)


def test_add_university(db):
    crud.add_university(db, "test1")
    university = crud.get_universities(db)[0]
    assert isinstance(university, models.University)
