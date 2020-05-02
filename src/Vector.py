from Node import Node
from Relationship import Relationship

class Vector:
    def __init__(self, name="", description="", relationships=[], checked_configuration=False,
                 checked_add_logentry=False, object_id=""):
        self.name = name
        self.description = description
        self.nodes = []
        self.relationships = relationships
        self.checked_configuration_table = checked_configuration
        self.checked_add_log_entry_table = checked_add_logentry
        self.object_id = object_id
        pass

    def add_node(self, node=None):
        if node is None:
            id = str(len(self.nodes)+1)
            node = Node(name="Node " + id, id=id)
        self.nodes.append(node)

    def add_relationship(self, relationship=None):
        id = str(len(self.relationships) + 1)
        if relationship is None:
            relationship = Relationship(name="Relationship" + id, id=id)
        elif relationship.id is None:
            relationship.id = id
        self.relationships.append(relationship)

    def get_nodes(self):
        return self.nodes

    def get_relationships(self):
        return  self.relationships

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def get_object_id(self):
        return self.object_id

    def set_object_id(self, id):
        self.object_id = id

    def is_checked_config(self):
        return self.checked_configuration_table

    def is_checked_add_log_entry(self):
        return self.checked_add_log_entry_table

    def to_dictionary(self):
        # Added node and relationship ids
        # Populate node object id list
        node_obj_ids = []
        for node in self.get_nodes():
            node_obj_ids.append(str(node.get_object_id()))
        # Populate relationships object id list
        relationship_obj_id = []
        for relation in self.get_relationships():
            relationship_obj_id.append(str(relation.get_object_id))

        out_dict = {"name": self.name, "description": self.description,
                    "checked configuration table": str(self.checked_configuration_table),
                    "checked add log entry table": str(self.checked_add_log_entry_table),
                    "node_obj_ids": node_obj_ids,
                    "relationship_obj_ids": relationship_obj_id}
        return out_dict

    def create_from_dictionary(dict):
        if dict["checked configuration table"] == "True":
            checked_configuration_table = True
        else:
            checked_configuration_table = False
        if dict["checked add log entry table"] == "True":
            checked_add_log_entry_table = True
        else:
            checked_add_log_entry_table = False

        return Vector(name=dict["name"], description=dict["description"],
                      checked_add_logentry=checked_add_log_entry_table,
                      checked_configuration=checked_configuration_table)
