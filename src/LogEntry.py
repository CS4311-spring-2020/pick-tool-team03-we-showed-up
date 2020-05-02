class LogEntry:

    def __init__(self, checked=False, serial=0, timestamp="", content="", host="", source="", sourcetype="",
                 vector_list=[]):
        self.checked = checked
        self.serial = serial
        self.timestamp = timestamp
        self.content = content
        self.host = host
        self.source = source
        self.sourcetype = sourcetype
        self.vector_list = vector_list

    def add_vector(self, num_vector):
        self.vector_list.append(num_vector)

    def get_vector_list_str(self):
        if len(self.vector_list)==0:
            return "N/A"

        str = ""
        for v in self.vector_list:
            str = str + str(v) + " "
        return str

    def to_list(self):
        return [str(self.serial), self.timestamp, self.content, self.host, self.source, self.sourcetype]
