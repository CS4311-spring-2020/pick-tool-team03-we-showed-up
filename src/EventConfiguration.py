from datetime import datetime

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

    def to_dictionary(self):
        out_dict = {"name": self.name, "description": self.description,
                    "starttime": self.starttime.strftime("%m/%d/%Y, %H:%M:%S"),
                    "endtime": self.endtime.strftime("%m/%d/%Y, %H:%M:%S"),
                    "rootpath": self.rootpath, "whitefolder": self.whitefolder,
                    "redfolder": self.redfolder, "bluefolder": self.bluefolder, "lead": self.lead,
                    "leadIP": self.leadIP, "connections": str(self.connections)}
        return out_dict

    def create_from_dictionary(dict):
        starttime = datetime.strptime(dict["starttime"], "%m/%d/%Y, %H:%M:%S")
        endtime = datetime.endtime(dict["starttime"], "%m/%d/%Y, %H:%M:%S")
        return EventConfiguration(name=dict["name"], description=dict["description"],
                                  starttime=starttime, endtime=endtime, rootpath=dict["rootpath"],
                                  whitefolder=dict["whitefolder"], redfolder=dict["redfolder"],
                                  bluefolder=dict["bluefolder"], lead=dict["lead"], leadIP=dict["leadIP"],
                                  connections=int(dict["connections"]))