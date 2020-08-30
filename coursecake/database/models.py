from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship


from ..scrapers.course import Course
from ..scrapers.course_class import CourseClass
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

    # Course id which is unique to the univerisity
    # It is not necessarily unique to the database,
    # Which is why university + id are primary keys
    id = Column(String, primary_key=True, nullable = False, index=True)
    title = Column(String, nullable = False)
    department = Column(String, nullable = False, index=True)

    # nullable fields
    units = Column(Integer, nullable = False)
    prerequisites_str = Column(String, nullable = False)
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
        self.id = course.id
        self.title = course.title
        self.department = course.department

        self.units = course.units

        self.prerequisites_str = course.prerequisites_str
        self.department_title = course.department_title
        self.restrictions = course.restrictions
        self.school = course.school


    def __repr__(self):
        return f"{self.id} | {self.units} | {self.term_id}\n"




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

    course_id = Column(String, ForeignKey("course.id"), nullable = False)

    # Class id which is unique to the univerisity
    # It is not necessarily unique to the database,
    # Which is why university + id are primary keys
    id = Column(String, primary_key=True, nullable = False, index=True)
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

    restrictions = Column(String, nullable = True)

    updated = Column(DateTime, default=datetime.utcnow)

    # relationships
    # prerequisites = relationship("Prerequisite", back_populates="courses")
    university = relationship("University", back_populates = "classes")
    course = relationship("Course", back_populates = "classes")



    def __init__(self, a_class: CourseClass, university: str, term: str):
        '''
        Courses uses a class objects
        See ../scraper/class.py
        '''
        self.university_name = university
        self.term_id = term
        self.id = a_class.id
        self.course_id = a_class.course_id

        self.instructor = a_class.instructor
        self.time = a_class.time
        self.location = a_class.location
        self.building = a_class.building
        self.room = a_class.room
        self.status = a_class.status
        self.type = a_class.type

        self.units = a_class.units
        self.max = a_class.max
        self.enrolled = a_class.enrolled
        self.waitlisted = a_class.waitlisted
        self.requested = a_class.requested



    def __repr__(self):
        return f"{self.id} | {self.instructor} | {self.units} | {self.status} | {self.term_id}\n"
