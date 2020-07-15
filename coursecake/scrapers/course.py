
class Course:
    '''
    All information needed to be collected about a course
    '''
    def __init__(self, courseDict = None):
        '''
        All None attributes must be provided
        Can be constructed as empty, from a dictionary
        '''
        ### Mandatory attributes ###

        ### Strings

        # The formal name of the course
        self.name = None

        # The Title of the course; more human readable
        self.title = None

        # The Course Code, often used in registration
        self.code = None

        self.department = None
        # Lecture / discussion / lab
        self.type = None
        self.instructor = None
        self.time = None
        self.location = None
        self.status = None

        ### Integers

        self.units = None

        ### Optional Attributes ###

        # time of final
        self.final = ""

        self.max = -1
        self.enrolled = -1
        self.waitlisted = 0
        self.requested = 0
        self.restrictions = ""

        if (courseDict != None):
            self.__initFromDict(courseDict)


    def __initFromDict(self, courseDict: dict):
        self.__dict__.update(courseDict)





    def isOpen(self) -> bool:
        '''
        Checks if course is open for registration
        '''
        return (self.status.lower().strip() == "open")



    def __str__(self) -> str:
        return f'''Course:
        {self.name}
        {self.title}
        {self.code}
        {self.type}
        {self.units}
        {self.instructor}
        {self.time}
        {self.location}
        {self.final}
        {self.max}
        {self.enrolled}
        '''





def main():
    course = Course()
    course.name = "yeet"
    course.title = "study of yeet"
    course.code = "1223"
    course.instructor = "mr.yeetus"

    print(course)


if __name__ == '__main__':
    main()
