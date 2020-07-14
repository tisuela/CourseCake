
class Course:
    def __init__(self):

        # The formal name of the course
        self.name = ""

        # The Title of the course; more human readable
        self.title = ""

        # The Course Code, often used in registration
        self.code = ""

        self.department = ""

        # Lecture / discussion / lab
        self.type = ""

        self.units = -1
        self.instructor = ""
        self.time = ""
        self.location = ""

        # time of final
        self.final = ""

        self.max = -1
        self.enrolled = -1
        self.waitlisted = 0
        self.requested = 0
        self.restrictions = ""
        self.status = ""


    def isOpen(self) -> bool:
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
