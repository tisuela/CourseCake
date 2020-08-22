from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


COURSES_DATABASE_URL = "sqlite:///../courses.db"

engine = create_engine(
# check same thread only needed for sqlite db
    COURSES_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
