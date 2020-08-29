from .course import Course

class CourseClass:
    '''
    All information needed to be collected about a course

    The best name for this class would be Class, but that would risk
    collisions with the python's class
    '''
    def __init__(self, course: Course, class_dict = None):
        '''
        All None attributes must be provided
        Can be constructed as empty, from a dictionary
        '''
        ### Mandatory attributes ###

        ### Strings

        # The formal name of the course
        self.course_id = course.id

        # The Class (also sometimes called course by some websites) Code, often used in registration
        self.id = None

        self.type = None
        self.instructor = None
        self.time = None

        # Full location string, with building  + room
        self.location = None
        self.building = None
        self.room = None
        self.status = None

        ### Integers

        self.units = None

        ### Optional Attributes ###
        # not necessarily nullable in our db models

        # time of final
        self.final = ""

        self.max = -1
        self.enrolled = -1
        self.waitlisted = 0
        self.requested = 0
        self.restrictions = ""
        self.school = ""



        if (class_dict != None):
            self._initFromDict(class_dict)


    def _init_from_dict(self, class_dict: dict):
        self.__dict__.update(class_dict)





    def isOpen(self) -> bool:
        '''
        Checks if course is open for registration
        '''
        return (self.status.lower().strip() == "open")


    def toInt(self, s: str) -> int:
        try:
            return int(s)
        except ValueError:
            return -1



    def __str__(self) -> str:
        return f'''CourseClass:
        {self.id}
        {self.course_id}
        {self.type}
        {self.units}
        {self.instructor}
        {self.time}
        {self.location}
        {self.final}
        {self.max}
        {self.enrolled}
        {self.status}
        '''
