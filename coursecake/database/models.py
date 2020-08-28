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
    classes = relationship("Class", back_populates = "university", lazy = "dynamic")



    def __repr__(self):
        return f"{self.name}"


class Course(Base):
    '''
    Courses have information that is mostly already covered in a Class.

    One Course can have many classes
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
    title = Column(String, nullable = False)
    department = Column(String, nullable = False, index=True)

    units = Column(Integer, nullable = False)

    # nullable fields

    department_title = Column(String, nullable = False)
    restrictions = Column(String, nullable = False)
    school = Column(String, nullable = False)

    updated = Column(DateTime, default=datetime.utcnow)

    # relationships
    # prerequisites = relationship("Prerequisite", back_populates="courses")
    university = relationship("University", back_populates = "courses")
    classes = relationship("Class", back_populates = "course", lazy = "dynamic")



    def __init__(self, course: Course, university: str, term: str):
        '''
        Courses uses a course objects
        See ../scraper/course.py
        '''
        self.university_name = university
        self.term_id = term
        self.code = course.code
        self.title = course.title
        self.department = course.department

        self.units = course.units
        self.department_title = course.department_title
        self.restrictions = course.restrictions
        self.school = course.school


    def __repr__(self):
        return f"{self.code} | {self.name} | {self.instructor} | {self.units} | {self.status} | {self.term_id}\n"




class Class(Base):
    '''
    This table is very detailed, getting all information we can possibly
    collect about a Class. Some information is already covered in Course,
    but this is more extensive.

    A class is the physical offering of a course, which includes instructor,
    time, location, etc.

    We include redundant information to easily query classes directly without
    joins from Course. Also some information such as "units" vary from what
    a Course may say. (One course might have two classes, a 4 unit lecture and
    a 2 unit lab. )
    '''

    __tablename__ = "class"

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

    course_code = Column(String, ForeignKey("course.code"), nullable = False)

    # Class code which is unique to the univerisity
    # It is not necessarily unique to the database,
    # Which is why university + code are primary keys
    code = Column(String, primary_key=True, nullable = False, index=True)
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

    restrictions = Column(String, nullable = False)

    updated = Column(DateTime, default=datetime.utcnow)

    # relationships
    # prerequisites = relationship("Prerequisite", back_populates="courses")
    university = relationship("University", back_populates = "classes")
    university = relationship("Course", back_populates = "classes")



    def __init__(self, class: Class, university: str, term: str):
        '''
        Courses uses a class objects
        See ../scraper/class.py
        '''
        self.university_name = university
        self.term_id = term
        self.code = class.code
        self.name = class.name
        self.department = class.department
        self.instructor = class.instructor
        self.time = class.time
        self.location = class.location
        self.building = class.building
        self.room = class.room
        self.status = class.status
        self.type = class.type

        self.units = class.units
        self.max = class.max
        self.enrolled = class.enrolled
        self.waitlisted = class.waitlisted
        self.requested = class.requested

        self.department_title = class.department_title
        self.restrictions = class.restrictions
        self.school = class.school


    def __repr__(self):
        return f"{self.code} | {self.name} | {self.instructor} | {self.units} | {self.status} | {self.term_id}\n"
