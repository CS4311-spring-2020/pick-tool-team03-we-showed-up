class Node:
    # Found this in the SRS :( "[SRS 45]	A node shall be part of at least one graph. "
    def __init__(self, id="", name="", timestamp="", description="", log_entry_reference="", log_creator="",
                 event_type="", source="", visibility=True, x=0, y=0):
        self.id = id
        self.name = name
        self.timestamp = timestamp
        self.description = description
        self.log_entry_reference = log_entry_reference
        self.log_creator = log_creator
        self.event_type = event_type
        self.source = source
        self.visibility = visibility
        self.x = x
        self.y = y
        pass

    def node_from_log_entry(log_entry):
        print("Must create node from given log entry")

