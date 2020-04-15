from Node import Node
from Relationship import Relationship

class Vector:
    def __init__(self, name="", description="", relationships=[], checked_configuration=False, checked_add_logentry=False):
        self.name = name
        self.description = description
        self.nodes = []
        self.relationships = relationships
        self.checked_configuration_table = checked_configuration
        self.checked_add_log_entry_table = checked_add_logentry
        pass

    def add_node(self, node=None):
        if node is None:
            id = str(len(self.nodes)+1)
            node = Node(name="Node " + id, id=id)
        self.nodes.append(node)

    def add_relationship(self, relationship=None):
        if relationship is None:
            id = str(len(self.relationships)+1)
            relationship = Relationship(name="Relationship" + id, id=id)
        self.relationships.append(relationship)

    def get_nodes(self):
        return self.nodes

    def get_relationships(self):
        return  self.relationships

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def is_checked_config(self):
        return self.checked_configuration_table

    def is_checked_add_log_entry(self):
        return self.checked_add_log_entry_table