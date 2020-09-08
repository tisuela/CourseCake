from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, scoped_session


from ..scrapers.course import Course as ClsCourse
from ..scrapers.course_class import CourseClass
from .sql import Base, SessionLocal

# TODO: RENAME IDs TO NOT BE IDS
class University(Base):
    """
    Holds redundant information, but might?? aid in future queries
    or refactors
    """

    __tablename__ = "university"

    # The university where this course is offered
    # This should be the university's domain name in all CAPS
    # Ex: UC Irvine's domain is uci.edu, so university = UCI
    name = Column(String, primary_key=True, nullable=False, index=True)
    courses = relationship("Course", back_populates="university", lazy="dynamic")
    classes = relationship("Class", back_populates="university", lazy="dynamic")

    def __repr__(self):
        return f"{self.name}"


class Course(Base):
    """
    Courses have information that is mostly already covered in a Class.

    One Course can have many classes
    """

    __tablename__ = "course"

    # The university where this course is offered
    # This should be the university's domain name in all CAPS
    # Ex: UC Irvine's domain is uci.edu, so university = UCI
    university_name = Column(String, ForeignKey("university.name"), nullable=False)

    # Term ID is: YEAR-SEASON-NUMBER
    # Ex: Summer session 2 would be 2020-SUMMER-2
    # Ex: Winter Quarter would be 2020-WINTER-1
    # Ex: Winter inter-term would also be 2020-WINTER(assuming no winter quarter)
    # Ex: Spring Semester would be 2020-SPRING-1
    # Specifying number is optional. If not specified, it is assumed to be 1.
    term_id = Column(String, nullable=False)
    # TODO: Add Term foreign key

    # Course id which is unique to the univerisity
    # It is not necessarily unique to the database,
    # Which is why university + id are primary keys
    course_id = Column(String, nullable=False, index=True)

    # This is university_name + term_id + course_id
    # Thus, this generates an ID unique in the entire database
    # This is critical to correctly join Course with Class
    # As such, this is used as the foreign key in Class
    primary_id = Column(String, primary_key=True)

    title = Column(String, nullable=False)
    department = Column(String, nullable=False, index=True)

    # nullable fields
    units = Column(Integer, nullable=False)
    prerequisites_str = Column(String, nullable=False)
    department_title = Column(String, nullable=False)
    restrictions = Column(String, nullable=False)
    school = Column(String, nullable=False)

    updated = Column(DateTime, default=datetime.utcnow)

    # relationships
    # prerequisites = relationship("Prerequisite", back_populates="courses")
    university = relationship("University", back_populates="courses")
    classes = relationship("Class", back_populates="course", lazy="subquery")

    def __init__(self, course: ClsCourse, university: str, term: str):
        """
        Courses uses a course objects
        See ../scraper/course.py
        """
        self.university_name = university
        self.term_id = term
        self.course_id = course.course_id

        self.primary_id = f"{self.university_name};{self.term_id};{self.course_id}"
        self.title = course.title
        self.department = course.department

        self.units = course.units

        self.prerequisites_str = course.prerequisites_str
        self.department_title = course.department_title
        self.restrictions = course.restrictions
        self.school = course.school

    def __repr__(self):
        return f"{self.course_id} | {self.units} | {self.term_id}\n"


# for GraphQL
Course.query = scoped_session(SessionLocal).query_property()


class Class(Base):
    """
    This table is very detailed, getting all information we can possibly
    collect about a Class. Some information is already covered in Course,
    but this is more extensive.

    A class is the physical offering of a course, which includes instructor,
    time, location, etc.

    We include redundant information to easily query classes directly without
    joins from Course. Also some information such as "units" vary from what
    a Course may say. (One course might have two classes, a 4 unit lecture and
    a 2 unit lab. )
    """

    __tablename__ = "class"

    # The university where this course is offered
    # This should be the university's domain name in all CAPS
    # Ex: UC Irvine's domain is uci.edu, so university = UCI
    university_name = Column(
        String, ForeignKey("university.name"), primary_key=True, nullable=False
    )

    # Term ID is: YEAR-SEASON-NUMBER
    # Ex: Summer session 2 would be 2020-SUMMER-2
    # Ex: Winter Quarter would be 2020-WINTER-1
    # Ex: Winter inter-term would also be 2020-WINTER(assuming no winter quarter)
    # Ex: Spring Semester would be 2020-SPRING-1
    # Specifying number is optional. If not specified, it is assumed to be 1.
    term_id = Column(String, primary_key=True, nullable=False)
    # TODO: Add Term

    course_id = Column(String, nullable=False)
    # TODO: Figure out multiple foreign keys
    course_primary_id = Column(String, ForeignKey("course.primary_id"), nullable=False)
    # Class id which is unique to the univerisity
    # It is not necessarily unique to the database,
    # Which is why university + id are primary keys
    class_id = Column(String, primary_key=True, nullable=False, index=True)
    instructor = Column(String, nullable=False)
    time = Column(String, nullable=False)
    location = Column(String, nullable=False)
    building = Column(String, nullable=False)
    room = Column(String, nullable=False)
    status = Column(String, nullable=False)
    type = Column(String, nullable=False)

    units = Column(Integer, nullable=False)
    max = Column(Integer, nullable=False)
    enrolled = Column(Integer, nullable=False)
    waitlisted = Column(Integer, nullable=False)
    requested = Column(Integer, nullable=False)

    # nullable fields

    updated = Column(DateTime, default=datetime.utcnow)

    # relationships
    # prerequisites = relationship("Prerequisite", back_populates="courses")
    university = relationship("University", back_populates="classes")
    course = relationship(
        "Course",
        back_populates="classes",
        foreign_keys=[course_primary_id],
        lazy="subquery",
    )

    def __init__(self, a_class: CourseClass, university: str, term: str):
        """
        Courses uses a class objects
        See ../scraper/class.py
        """
        self.university_name = university
        self.term_id = term
        self.class_id = a_class.class_id
        self.course_id = a_class.course_id
        self.course_primary_id = (
            f"{self.university_name};{self.term_id};{self.course_id}"
        )

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
        return f"{self.class_id} | {self.instructor} | {self.units} | {self.status} | {self.term_id}\n"


# for GraphQL
Class.query = scoped_session(SessionLocal).query_property()
