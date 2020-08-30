from ..course_class import CourseClass

class UciClass(CourseClass):
    '''
    This class is used to construct Course objects from Uci's course schedule,
    WEBSOC. No attributes are added, but helper methods and __init__ will be
    modified / added to help with construction
    '''
    # TODO: FIX PARAMETERS!!!!
    def __init__(self, course_id: str, cells = None, class_dict: dict = None):


        if (class_dict != None):
            CourseClass.__init__(self, course_id, class_dict)
        else:
            CourseClass.__init__(self, course_id)

        if (cells != None):
            self._init_from_cells(cells)



    def _init_from_cells(self, cells):

        self.id = cells[0].text
        self.type = cells[1].text
        self.units = self.toInt(cells[3].text.split("/")[-1])
        self.instructor = cells[4].get_text(separator="; ")
        self.time = " ".join(cells[5].text.strip().split())

        # Get location
        self.location = cells[6].text.strip().upper()
        self.building = self.location.rsplit(" ",1)[0]
        self.room = self.location.rsplit(" ",1)[-1]

        self.final = cells[7].text.strip()

        # Enrollment info
        self.max = self.toInt(cells[8].text)
        self.enrolled = self.toInt(cells[9].text.split("/")[-1])
        self.waitlisted = self.toInt(cells[10].text)
        self.requested_waitlisted = self.toInt(cells[11].text)
        self.status = cells[-1].text
