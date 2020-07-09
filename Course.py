
class Course:
    def __init__(self):

        # The formal name of the course
        self.name = ""

        # The Title of the course; more human readable
        self.title = ""

        # The Course Code, often used in registration
        self.code = ""

        self.instructor = ""
        self.time = ""
        self.location = ""


    def __str__(self) -> str:
        return f"Course:\n    {self.name}\n    {self.code}\n    {self.instructor}\n    {self.location}"





def main():
    course = Course()
    course.name = "yeet"
    course.code = "1223"

    print(course.__dict__)


if __name__ == '__main__':
    main()
