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
