

class Relationship:
    def __init__(self, name="", id=0, parent=None, child=None, object_id=0x0):
        self.name = name
        self.id = id
        self.parent = parent
        self.child = child
        self.object_id = object_id
        pass

    def get_parent_name(self):
        if self.parent is None:
            return ""
        return self.parent.name

    def get_parent_id(self):
        if self.parent is None:
            return ""
        return self.parent.get_id()


    def get_child_name(self):
        if self.child is None:
            return ""
        return self.child.name

    def get_child_id(self):
        if self.child is None:
            return ""
        return self.child.get_id()

    def get_id_str(self):
        return str(self.id)

    def get_name(self):
        return self.name

    def get_object_id(self):
        return self.object_id

    def set_object_id(self, id):
        self.object_id = id

    def to_dictionary(self):
        """Exports a dictionary of the attributes of the object."""
        out_dict = {"id": self.get_id_str(), "name": self.get_name(),
                    "child id": str(self.get_child_id()), "parent id": str(self.get_parent_id())}
        return out_dict

    def create_from_dictionary(dict):
        """Creates a new relationship object given a dictionary format."""
        return Relationship(id=int(dict["id"]), name=dict["name"])
