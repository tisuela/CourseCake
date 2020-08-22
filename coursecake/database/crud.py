# all operations to db are here
from sqlalchemy.orm import Session

from . import models



def get_universities(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.University).offset(offset).limit(limit).all()



def add_university(db: Session, name: str) -> models.University:
    university = models.University(name=name)
    db.add(university)
    db.commit()
    db.refresh(university)
    return university
