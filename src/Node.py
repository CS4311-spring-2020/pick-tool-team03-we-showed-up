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

    def get_log_creator(self):
        return str(self.log_creator)

    def get_name(self):
        return str(self.name)

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

    def get_visibility_string(self):
        return str(self.visibility)

    def to_dictionary(self):
        out_dict = {"id": self.id, "name": self.name, "timestamp": self.get_timestamp(),
                    "description": self.description, "log entry reference": self.log_entry_reference,
                    "log creator": self.log_creator, "event type": self.event_type, "source": self.source,
                    "icon type": self.icon_type, "visibility": self.get_visibility_string(), "x": str(self.x),
                    "y": str(self.y)}
        return out_dict

    def create_from_dictionary(dict):
        if dict["visibility"] == "True":
            visibility = True
        else:
            visibility = False

        timestamp = dict["timestamp"]
        return Node(id=dict["id"], name=dict["name"], timestamp=timestamp, description=dict["description"],
                    log_entry_reference=dict["log entry reference"], log_creator=dict["log creator"],
                    event_type=dict["event type"], source=dict["source"], icon_type=dict["icon type"],
                    visibility=visibility, x=float(dict["x"]), y=float(dict["y"]))

