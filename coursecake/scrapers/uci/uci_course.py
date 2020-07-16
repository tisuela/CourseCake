from ..course import Course


class UCICourse(Course):
    def __init__(self, cells = None, templateCourse = None, courseDict = None):


        if (templateCourse != None):
            Course.__init__(self, templateCourse.__dict__)
        else:
            Course.__init__(self, courseDict)

        if (cells != None):
            self.__initFromCells(cells)



    def __initFromCells(self, cells):
        self.code = cells[0].text
        self.type = cells[1].text
        self.units = self.toInt(cells[3].text)
        self.instructor = cells[4].text
        self.time = " ".join(cells[5].text.strip().split())
        self.location = cells[6].text.strip()
        self.final = cells[7].text.strip()
        self.max = self.toInt(cells[8].text)
        self.enrolled = self.toInt(cells[9].text.split("/")[-1])
        self.waitlisted = self.toInt(cells[10].text)
        self.requestedwaitlisted = self.toInt(cells[11].text)
        self.status = cells[-1].text
