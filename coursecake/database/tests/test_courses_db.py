import pytest
from sqlalchemy.orm import Session

from .. import crud, models
from ..sql import SessionLocal, engine


class University:

    def __init__(self, name):
        self.name = name

university = University("test1")

@pytest.fixture(scope="module")
def db():
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    models.Base.metadata.drop_all(bind=engine)


def test_add_university(db):
    crud.add_university(db, **university.__dict__)
    universityRow = crud.get_universities(db)[0]
    print("result", universityRow)
    assert isinstance(universityRow, models.University)
