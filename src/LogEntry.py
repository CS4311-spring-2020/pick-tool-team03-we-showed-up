import random


class LogEntry:

    def __init__(self, number=random.randint(0, 10000), timestamp="", content="", host="", source="", sourcetype=""):
        self.number = number
        self.timestamp = timestamp
        self.content = content
        self.host = host
        self.source = source
        self.sourcetype = sourcetype
