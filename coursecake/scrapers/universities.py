import json

"""
writes and obtains data on university needed for scraping.
Ex: course schedule link, catalogue link, etc.
"""


class Universities:
    def __init__(self):
        self.jsonFileName = "./coursecake/scrapers/universities.json"

    def getData(self) -> dict:
        """
        Gets existing university data
        Returns empty dict if file does not exist
        """
        data = dict()

        with open(self.jsonFileName, "r") as jsonFile:
            data = json.load(jsonFile)
        jsonFile.close()

        return data

    def getUniversity(self, name: str):
        name = name.upper()
        try:
            return self.getData()[name]
        except KeyError:
            return "university name and info not in database"
        except FileNotFoundError as e:
            return f"file not found, message: \n {e}"

    def add(self, name: str, **kwargs) -> None:
        """
        Add a new university to the json file
        """

        try:
            # get existing data
            data = self.getData()
            name = name.upper()

            if data.get(name) != None:
                # override existing info
                data[name].update(kwargs)
            else:
                # if new university, create it
                data[name] = kwargs
        except FileNotFoundError as e:
            data = dict()

        with open(self.jsonFileName, "w+") as jsonFile:
            json.dump(data, jsonFile)

        jsonFile.close()


"""
def main():
    adder = Universities()
    data = adder.getData()

    # template denoting what info is required for every uni
    template = dict()
    info = dict()

    # if an existing university has info containing more
    # than one element, it is eligible to be a template
    for key,value in data.items():
        if (len(value) > 1):
            template = value
            break

    name = input("New University name: ")

    # if there is a template, do this
    if (len(template) > 1 and type(template) is dict):
        for key in template.keys():
            info[key] = input(f"Insert new univeristy {key}: ")

    else:
        while True:
            key = input("What is the name/key for this information? ")
            value = input("What is the value/info?  ")
            info.update({key: value})

            moreInfo = input("Do you have more info? (y/n): ")
            if (moreInfo.lower() not in ["yes", "y", "ye"]):
                break



    adder.add(name, **info)



if __name__ == '__main__':
    main()
"""
