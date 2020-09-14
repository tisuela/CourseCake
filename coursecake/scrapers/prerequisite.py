class Prerequisite:
    def __init__(self, type: str, courses: list, prerequisiteTo: str):
        # courses in this prereqs are either AND or OR
        self.type = type

        # list of courses that can satisfy this prerequisite
        # courses are course names
        self.courses = courses

        # Course ID
        self.prerequisiteTo = prerequisiteTo


"""
notes:

"""
