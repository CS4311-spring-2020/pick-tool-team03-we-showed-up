class EventConfiguration:

    def __init__(self, name="", description="", starttime="", endtime="", rootpath="", whitefolder="", redfolder="",
                 bluefolder="", lead=True, leadIP="", connections=0):
        self.name = name
        self.description = description
        self.starttime = starttime
        self.endtime = endtime
        self.rootpath = rootpath
        self.whitefolder = whitefolder
        self.redfolder = redfolder
        self.bluefolder = bluefolder
        self.lead = lead
        self.leadIP = leadIP
        self.connections = connections

    # Checks if all the attributes are filled
    def is_complete(self):
        dict = self.__dict__()
        for i in dict.values():
            if i == "":
                return False
        return True

    def get_name(self):
        return self.name

    def get_start(self):
        return self.starttime

    def get_end(self):
        return self.endtime
