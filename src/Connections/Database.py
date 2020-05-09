from EventConfiguration import EventConfiguration
from Node import Node
from Relationship import Relationship
from Vector import Vector
from pymongo import MongoClient
from bson import Binary, Code, ObjectId
from bson.json_util import dumps
from bson.json_util import loads


class Database:
    """This class serves as an interface with the Mongo database in order to retrieve, update and delete the data
    of the event."""

    def __init__(self):
        # Connection to mongo server
        self.client = MongoClient('mongodb://localhost')
        # connection to mongo database
        self.pick_database = self.client['PICK-Tool-Vector-Database']

        # Collections
        # Event configuration collection
        self.pick_eventconfig = self.pick_database['event_configuration']
        # Node collection
        self.pick_nodes = self.pick_database['nodes']
        # Relationship collection
        self.pick_relationships = self.pick_database['relationships']
        # Vector collection
        self.pick_vectors = self.pick_database['vectors']

    def get_event_map(self):
        """Returns map containing the event names as keys and IDs as values."""
        event_dicts = list(self.pick_eventconfig.find())
        event_map = {}
        for e in event_dicts:
            event_map[e.get('name')] = e.get('_id')
        return event_map

    def get_event_names(self):
        """Retrieves the names of the events and exports them as a list."""
        return list(self.get_event_map().keys())

    def save_vector_to_database(self, vector):
        """Inserts vector into the vector collection of the db."""
        # Insert node dictionary
        for node in vector.get_nodes():
            self.save_node_to_database(node)

        # Insert relationship dictionary
        for relationship in vector.get_relationships():
            self.save_relationship_to_database(relationship)

        result_vect = self.pick_vectors.insert_one(vector.to_dictionary())
        obj_id = result_vect.inserted_id
        vector.set_object_id(obj_id)
        return obj_id

    def save_node_to_database(self, node):
        """Inserts node into the node collection of the db."""
        node_result = self.pick_nodes.insert_one(node.to_dictionary())
        print("saved node with objid:", node_result.inserted_id)
        node_id = node_result.inserted_id
        node.set_object_id(node_id)
        return node.get_object_id()

    def save_relationship_to_database(self, relationship):
        """Inserts the relationship into the relationship collection of the db."""
        relationship_result = self.pick_relationships.insert_one(relationship.to_dictionary())
        print("saved relationship with objid: ", relationship_result.inserted_id)
        relationship_id = relationship_result.inserted_id
        relationship.set_object_id(relationship_id)
        return relationship.get_object_id()

    def save_event_data_to_database(self, event_config, vector_list):
        """Inserts all the event data into the respective collection of the db."""
        print("saving event data of: ", event_config.name)
        vector_obj_ids = list()

        for vector in vector_list:
            vector_obj_ids.append(self.save_vector_to_database(vector))

        ec_dict = event_config.to_dictionary(vector_obj_ids)

        result = self.pick_eventconfig.insert_one(ec_dict)
        obj_id = result.inserted_id
        print(obj_id)
        event_config.set_object_id(obj_id)
        print(event_config.object_id)

    def get_event_data(self, event_id):
        """Retrieves the complete event data given an event ID, returns it in a dictionary with the event
        config and the vectors list"""
        # Retrieve event config
        ec_test = self.get_event_config(event_id)
        if ec_test is None:
            print("Invalid ID")
            return
        event_config = EventConfiguration.create_from_dictionary(ec_test)
        event_config.set_object_id(event_id)

        # Get Vector ID list
        vector_id_list = ec_test.get("vector_obj_ids")

        vector_list = []
        for id in vector_id_list:
            vdict = self.get_vector(id)
            vector = Vector.create_from_dictionary(vdict)
            vector.set_object_id(id)
            node_id_list = vdict.get("node_obj_ids")
            relationship_id_list = vdict.get("relationship_obj_ids")

            nodes_map = {}
            for n_id in node_id_list:
                ndict = self.get_node(n_id)
                node = Node.create_from_dictionary(ndict)
                node.set_object_id(n_id)
                nodes_map[node.get_id()] = node
                vector.add_node(node)
            for r_id in relationship_id_list:
                rdict = self.get_relationship(r_id)
                relationship = Relationship.create_from_dictionary(rdict)
                relationship.set_object_id(r_id)
                relationship.child = nodes_map[rdict.get('child id')]
                relationship.parent = nodes_map[rdict.get('parent id')]
                vector.add_relationship(relationship)

            vector_list.append(vector)

        out_map = {"event_config": event_config, "vectors": vector_list}
        return out_map

    # Retrieve specific information from database
    def get_vector(self, vector_id):
        vector_result = self.pick_vectors.find_one({"_id": ObjectId(str(vector_id))})
        return vector_result

    def get_node(self, node_id):
        node_result = self.pick_nodes.find_one({"_id": ObjectId(str(node_id))})
        return node_result

    def get_relationship(self, relation_id):
        relation_result = self.pick_relationships.find_one({"_id": ObjectId(str(relation_id))})
        return relation_result

    def get_event_config(self, ec_id):
        ec_result = self.pick_eventconfig.find_one({"_id": ObjectId(ec_id)})
        return ec_result

    def update_event(self, event_config, vectors):

        # if event is not saved, then save it and return
        if event_config.get_object_id() == 0x0:
            print("Event wasn't saved, saving it now: ", event_config.name)
            return self.save_event_data_to_database(event_config, vectors)

        print("Updating event: ", event_config.name)
        vector_id_list = list()
        for vector in vectors:
            vector_id_list.append(self.update_vector(vector))
        self.update_event_config(event_config, vector_id_list)

    def update_event_config(self, event_config, vector_id_list):
        print(event_config.get_object_id())
        self.pick_eventconfig.replace_one({"_id": event_config.get_object_id()},
                                          event_config.to_dictionary(vector_id_list))

    def update_vector(self, vector):
        print("updating vector:", vector.name)
        # if node isn't in the database, add it
        if vector.get_object_id() == 0x0:
            return self.save_vector_to_database(vector)
        # Update vector
        node_list = vector.get_nodes()
        relationship_list = vector.get_relationships()
        # update nodes in vector
        for node in node_list:
            self.update_node(node)
        # update relationships in vector
        for relation in relationship_list:
            self.update_relationships(relation)

        vector_dict = vector.to_dictionary()
        print("vector id is: ", vector.object_id)
        vector_result = self.pick_vectors.update_one({"_id": vector.object_id},
                                                     {"$set": {"name": vector.name, "description": vector.description,
                                                               "checked configuration table": str(
                                                                   vector.checked_configuration_table),
                                                               "checked add log entry table": str(
                                                                   vector.checked_add_log_entry_table),
                                                               "node_obj_ids": vector_dict.get("node_obj_ids"),
                                                               "relationship_obj_ids": vector_dict.get(
                                                                   "relationship_obj_ids")}})
        print("node id list is now", vector_dict.get("node_obj_ids"))
        return vector.get_object_id()

    def update_node(self, node):
        print("updating node: ", node.name)
        # if node isn't in the database, add it
        if node.get_object_id() == 0x0:
            print("node wasn't in db, adding it:", node.name)
            return self.save_node_to_database(node)
        node_dict = self.get_node(node.get_object_id())

        node_result = self.pick_nodes.update_one({"_id": ObjectId(node_dict.get("_id"))},
                                                 {"$set": {"name": node.get_name(),
                                                           "timestamp": node.get_timestamp(),
                                                           "description": node.description,
                                                           "log entry reference": node.log_entry_reference,
                                                           "log creator": node.log_creator,
                                                           "event type": node.event_type,
                                                           "source": node.source, "icon type": node.icon_type,
                                                           "visibility": node.get_visibility_string(),
                                                           "x": str(node.x), "y": str(node.y)}})
        return node.get_object_id()

    def update_relationships(self, relationship):
        # if relationship isn't in database, add it
        if relationship.get_object_id() == 0x0:
            print("relationship wasn't in db, adding it:", relationship.name)
            return self.save_relationship_to_database(relationship)
        relation_dict = self.get_relationship(relationship.get_object_id())

        relationship_result = self.pick_relationships.update_one({"_id": ObjectId(relation_dict.get("_id"))},
                                                                 {"$set": {"name": relationship.get_name(),
                                                                           "child": relationship.get_child_id(),
                                                                           "parent": relationship.get_parent_id()}})
        return relationship.get_object_id()

    # Delete data from mongo database
    # NOTE: needs consultation with the team to determine the field through which the vector will be found
    # and deleted
    def delete_vector(self, node_id, relationship_id, vector_id, ec_id):
        # Delete node
        node_result = self.pick_nodes.delete_one({"_id": ObjectId(str(node_id))})
        # Delete relationship
        relationship_result = self.pick_relationships.delete_one({"_id": ObjectId(str(relationship_id))})
        # Delete vector
        vector_result = self.pick_vectors.delete_one({"_id": ObjectId(str(vector_id))})
        # Delete event config
        ec_result = self.pick_eventconfig.delete_one({"_id": ObjectId(str(ec_id))})

    # Serialize dictionaries (event configuration, node, relationship, vector) using JSON
    # FIXME
    def serialize_eventconfig(self, ec_dictionary):
        temp_ec_dictionary = ec_dictionary
        app_json = dumps(temp_ec_dictionary)
        print(app_json)
        return app_json

    def serialize_node(self, node_dictionary):
        temp_node_dictionary = node_dictionary
        app_json = dumps(temp_node_dictionary)
        print(app_json)
        return app_json

    def serialize_relationship(self, relationship_dictionary):
        temp_relationship_dictionary = relationship_dictionary
        app_json = dumps(temp_relationship_dictionary)
        print(app_json)
        return app_json

    def serialize_vector(self, vector_dictionary):
        temp_vector_dictionary = vector_dictionary
        app_json = dumps(temp_vector_dictionary)
        print(app_json)
        return app_json

    # Deserialize dictionaries (event configuration, node, relationship, vector) using JSON
    # FIXME
    def deserialize_eventconfig(self, ec_dictionary):
        decoded_ec_dictionary = ec_dictionary
        decode_json_ec = loads(decoded_ec_dictionary)
        print(decode_json_ec)
        return decode_json_ec

    def deserialize_node(self, node_dictionary):
        decoded_node_dictionary = node_dictionary
        decode_json_node = loads(decoded_node_dictionary)
        print(decode_json_node)
        return decode_json_node

    def deserialize_relationship(self, relationship_dictionary):
        decoded_relationship_dictionary = relationship_dictionary
        decode_json_rel = loads(decoded_relationship_dictionary)
        print(decode_json_rel)
        return decode_json_rel

    def deserialize_vector(self, vector_dictionary):
        decode_vector_dictionary = vector_dictionary
        decode_json_vec = loads(decode_vector_dictionary)
        print(decode_json_vec)
        return decode_json_vec

    # Export vector collection
    def export_vector_collection(self, ec_id):
        # Export vector collection (this is not how you do it though...)
        pick_datacollection = self.pick_database['pick_collection']
        ec_result = self.pick_eventconfig.find_one({"_id": ObjectId(str(ec_id))})
        pick_collection_result = pick_datacollection.insert_one(ec_result)
        return pick_collection_result
