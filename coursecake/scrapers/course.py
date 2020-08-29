import copy

class Course:
    '''
    All information needed to be collected about a course
    '''
    def __init__(self, course_dict = None, course = None, ):
        '''
        All None attributes must be provided
        Can be constructed as empty, from a dictionary
        '''
        ### Mandatory attributes ###


        ### Strings

        # The formal name of the course which acts as an ID
        self.id = None

        # The Title of the course; more human readable
        self.title = None

        self.department = None

        ### Integers

        self.units = None

        ### Optional Attributes ###
        # nullable in our db models
        self.classes = list()

        self.restrictions = ""
        self.school = ""

        # a more readable department name
        # Ex: COMSPSCI -> Computer Science
        self.department_title = ""

        if (course_dict != None):
            self._init_from_dict(course_dict)

        if (course != None):
            self._init_from_dict(course.__dict__)

            # must deep copy list
            self.classes = copy.deepcopy(course.classes)


    def _init_from_dict(self, course_dict: dict):
        self.__dict__.update(course_dict)


    def is_valid_course(self) -> bool:
        for value in self.__dict__.values():
            if value == None:
                return False

        return True



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
        return f'''Course:
        {self.title}
        {self.id}
        {self.units}
        '''
