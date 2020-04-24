

class Relationship:
    def __init__(self, name="", id=0, parent=None, child=None):
        self.name = name
        self.id = id
        self.parent = parent
        self.child = child
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
