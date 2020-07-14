import json



class Universities:
    def __init__(self):
        self.jsonFileName = "./coursecake/scrapers/universities.json"


    def getData(self) -> dict:
        '''
        Gets existing university data
        Returns empty dict if file does not exist
        '''
        data = dict()

        with open(self.jsonFileName, "r") as jsonFile:
            data = json.load(jsonFile)
        jsonFile.close()

        return data



    def getUniversity(self, name: str) -> str:
        try:
            return self.getData()[name]
        except KeyError:
            return "university name and url not in database"
        except FileNotFoundError as e:
            return f"file not found, message: \n {e}"


    def add(self, name: str, course_website: str) -> None:
        '''
        Add a new university to the json file
        '''
        newUniversity = {name: course_website}

        try:
            data = self.getData()
            data.update(newUniversity)
        except FileNotFoundError as e:
            data = dict()

        with open(self.jsonFileName, "w+") as jsonFile:
            json.dump(data, jsonFile)


        jsonFile.close()





def main():
    adder = Universities()
    name = input("New University name: ")
    course_website = input("New University course website: ")
    adder.add(name, course_website)



if __name__ == '__main__':
    main()
