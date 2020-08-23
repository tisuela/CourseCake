from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship


from ..scrapers.course import Course
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
    courses = relationship("Course", back_populates = "university", lazy = "dynamic")



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
    university_name = Column(String, ForeignKey("university.name"), primary_key=True,  nullable = False)

    # Term ID is: YEAR-SEASON-NUMBER
    # Ex: Summer session 2 would be 2020-SUMMER-2
    # Ex: Winter Quarter would be 2020-WINTER-1
    # Ex: Winter inter-term would also be 2020-WINTER(assuming no winter quarter)
    # Ex: Spring Semester would be 2020-SPRING-1
    # Specifying number is optional. If not specified, it is assumed to be 1.
    term_id = Column(String, primary_key=True, nullable = False)
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

    department_title = Column(String, nullable = False)
    restrictions = Column(String, nullable = False)
    school = Column(String, nullable = False)

    updated = Column(DateTime, default=datetime.utcnow)

    # relationships
    # prerequisites = relationship("Prerequisite", back_populates="courses")
    university = relationship("University", back_populates = "courses")



    def __init__(self, course: Course, university: str, term: str):
        '''
        Courses uses a course objects
        See ../scraper/course.py
        '''
        self.university_name = university
        self.term_id = term
        self.code = course.code
        self.name = course.name
        self.title = course.title
        self.department = course.department
        self.instructor = course.instructor
        self.time = course.time
        self.location = course.location
        self.building = course.building
        self.room = course.room
        self.status = course.status
        self.type = course.type

        self.units = course.units
        self.max = course.max
        self.enrolled = course.enrolled
        self.waitlisted = course.waitlisted
        self.requested = course.requested

        self.department_title = course.department_title
        self.restrictions = course.restrictions
        self.school = course.school


    def __repr__(self):
        return f"{self.code} | {self.name} | {self.instructor} | {self.units} | {self.status} | {self.term_id}\n"
