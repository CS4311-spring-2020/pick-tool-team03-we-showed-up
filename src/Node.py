import datetime


class Node:
    # Found this in the SRS :( "[SRS 45]	A node shall be part of at least one graph. "
    def __init__(self, id="", name="", timestamp=datetime.datetime.now(), description="", log_entry_reference="", log_creator="",
                 event_type="", source="", icon_type="", icon=None, visibility=True, x=0, y=0):
        self.id = id
        self.name = name
        self.timestamp = timestamp
        self.description = description
        self.log_entry_reference = log_entry_reference
        self.log_creator = log_creator
        self.event_type = event_type
        self.source = source
        self.icon_type = icon_type
        self.visibility = visibility
        self.icon = icon
        self.x = x
        self.y = y
        pass

    def is_visible(self):
        return self.visibility

    def node_from_log_entry(log_entry):
        print("Must create node from given log entry")
        id = log_entry.serial
        return Node(
            id=id, name="Node " + str(id),
            timestamp=log_entry.timestamp,
            description=log_entry.content,
            log_entry_reference=log_entry.serial,
            log_creator=log_entry.source,
            source=log_entry.source,
            event_type=log_entry.sourcetype,
        )

    def get_id(self):
        return str(self.id)

    def get_reference(self):
        return str(self.log_entry_reference)

    def get_timestamp(self):
        if isinstance(self.timestamp, datetime.date):
            return self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        return self.timestamp

    def set_icon(self, icon):
        self.icon = icon
        # TODO: set icontype according to this