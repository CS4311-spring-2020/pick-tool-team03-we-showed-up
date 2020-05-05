from datetime import datetime
import time

class EventConfiguration:

    def __init__(self, name="", description="", starttime="", endtime="", rootpath="", whitefolder="", redfolder="",
                 bluefolder="", lead=True, leadIP="", connections=0, object_id=0x0):
        self.object_id = object_id
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

    def get_object_id(self):
        return self.object_id

    def set_object_id(self, id):
        self.object_id = id

    def to_dictionary(self, vector_id_list):
        temp_vector_id_list = vector_id_list
        out_dict = {"name": self.name, "description": self.description,
                    "starttime": self.starttime,
                    "endtime": self.endtime,
                    "rootpath": self.rootpath, "whitefolder": self.whitefolder,
                    "redfolder": self.redfolder, "bluefolder": self.bluefolder, "lead": self.lead,
                    "leadIP": self.leadIP, "connections": str(self.connections),
                    "vector_obj_ids": temp_vector_id_list}
        return out_dict

    def create_from_dictionary(dict):
        if dict["starttime"] is str:
            starttime = datetime.strptime(dict["starttime"], "%m/%d/%Y, %H:%M:%S")
        else:
            starttime = dict["starttime"]
        if dict["endtime"] is str:
            endtime = datetime.strptime(dict["endtime"], "%m/%d/%Y, %H:%M:%S")
        else:
            endtime = dict["endtime"]
        return EventConfiguration(name=dict["name"], description=dict["description"],
                                  starttime=starttime, endtime=endtime, rootpath=dict["rootpath"],
                                  whitefolder=dict["whitefolder"], redfolder=dict["redfolder"],
                                  bluefolder=dict["bluefolder"], lead=dict["lead"], leadIP=dict["leadIP"],
                                  connections=int(dict["connections"]))
