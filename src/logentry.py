class LogEntry:

    def __init__(self, serial=0, timestamp="", content="", host="", source="", sourcetype=""):
        self.serial = serial
        self.timestamp = timestamp
        self.content = content
        self.host = host
        self.source = source
        self.sourcetype = sourcetype
