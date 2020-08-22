from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .sql import Base

class University(Base):
    '''
    Holds redundant information, but might?? aid in future queries
    or refactors
    '''
    __tablename__ = "university"

    # The university where this course is offered
    # This should be the university's domain name in all CAPS
    # Ex: UC Irvine's domain is uci.edu, so university = UCI
    name = Column(String, primary_key=True, nullable = False, index=True)
    # courses = relationship("Course", back_populates = "university")



    def __repr__(self):
        return f"{self.name}"


class Course(Base):
    '''
    This table is very detailed, getting all information we can possibly
    collect about a Course. It may be better practice to separate it to
    multiple tables, but we are not worried about database size right now.
    We want all course information to be easily accessed from one model
    without having to join multiple tables

    To compensate, other tables will be made (like University) whose
    information is redundant but will aid in query performance.
    '''

    __tablename__ = "course"

    # The university where this course is offered
    # This should be the university's domain name in all CAPS
    # Ex: UC Irvine's domain is uci.edu, so university = UCI
    university = Column(String, ForeignKey("university.name"), primary_key=True,  nullable = False)

    # TODO: Add Term

    # Course code which is unique to the univerisity
    # It is not necessarily unique to the database,
    # Which is why university + code are primary keys
    code = Column(String, primary_key=True, nullable = False, index=True)
    name = Column(String, nullable = False)
    title = Column(String, nullable = False)
    department = Column(String, nullable = False, index=True)
    instructor = Column(String, nullable = False)
    time = Column(String, nullable = False)
    location = Column(String, nullable = False)
    building = Column(String, nullable = False)
    room = Column(String, nullable = False)
    status = Column(String, nullable = False)
    type = Column(String, nullable = False)

    units = Column(Integer, nullable = False)
    max = Column(Integer, nullable = False)
    enrolled = Column(Integer, nullable = False)
    waitlisted = Column(Integer, nullable = False)
    requested = Column(Integer, nullable = False)

    # nullable fields

    departmentTitle = Column(String, nullable = False)
    restrictions = Column(String, nullable = False)
    school = Column(String, nullable = False)

    updated = Column(DateTime, default=datetime.utcnow)

    # relationships
    # prerequisites = relationship("Prerequisite", back_populates="courses")





    def __repr__(self):
        return f"{self.code} | {self.name} | {self.instructor} | {self.units} | {self.status} \n"
