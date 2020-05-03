from EventConfiguration import EventConfiguration
from Node import Node
from Relationship import Relationship
from Vector import Vector

from pymongo import MongoClient
from bson import Binary, Code, ObjectId
from bson.json_util import dumps
from bson.json_util import loads


class Database:
    # Make connection and get data to be inserted
    def __init__(self):
        # Connection to mongo server
        self.client = MongoClient('mongodb://localhost')
        # connection to mongo database
        self.pick_database = self.client['PICK-Tool-Vector-Database']

        # Objects
        # Event configuration
        self.ec = EventConfiguration()
        # Node
        self.node = Node()
        # Relationship
        self.relationship = Relationship()
        # Vector
        self.vector = Vector()

        # Dictionaries
        # Event configuration dictionary
        self.ec_dictionary = self.ec.to_dictionary()
        # Node dictionary
        self.node_dictionary = self.node.to_dictionary()
        # Relationship dictionary
        self.relationship_dictionary = self.relationship.to_dictionary()
        # Vector dictionary
        self.vector_dictionary = self.vector.to_dictionary()

        # Collections
        # Event configuration collection
        self.pick_eventconfig = self.pick_database['event_configuration']
        # Node collection
        self.pick_nodes = self.pick_database['nodes']
        # Relationship collection
        self.pick_relationships = self.pick_database['relationships']
        # Vector collection
        self.pick_vectors = self.pick_database['vectors']

    # Retrieve database

    # Insert data to mongo database
    def save_vector_to_database(self, vector):
        # Insert node dictionary
        for node in vector.get_nodes():
            node_result = self.pick_nodes.insert_one(node.to_dictionary())
            print(node_result.inserted_id)
            node_id = node_result.inserted_id
            self.node.set_object_id(str(node_id))

        # Insert relationship dictionary
        for relationship in vector.get_relationships():
            relationship_result = self.pick_relationships.insert_one(relationship.to_dictionary())
            print(relationship_result.inserted_id)
            relationship_id = relationship_result.inserted_id
            self.relationship.set_object_id(str(relationship_id))

        result_vect = self.pick_vectors.insert_one(vector.to_dictionary())
        obj_id = result_vect.inserted_id
        vector.set_object_id(obj_id)
        return obj_id

    def save_event_config_to_database(self, event_config, vector_list):
        vector_obj_ids = list()

        for vector in vector_list:
            vector_obj_ids.append(self.save_vector_to_database(vector))
        # at this point, the vector_obj_ids list has all the object ids of all the vectors in the event

        ec_dict = event_config.to_dictionary()
        print(ec_dict['name'])
        ec_dict['vector_obj_ids'] = str(vector_obj_ids)

        result = self.pick_eventconfig.insert_one(ec_dict)

    # Update data from mongo database
    # NOTE: needs consultation with the team since multiple items in the vector can be updated
    def update_vector(self, node_id, relationship_id, vector_id):
        # Update event config
        # NOTE: for update and delete, we take the object_id directly from the objects rather than the dictionary
        # Update node
        node_result = self.pick_nodes.update_one({"_id": ObjectId(self.node.object_id)},
                                                 {"$set": {"name": node_id}})
        # Update relationship
        relationship_result = self.pick_relationships.update_one({"_id": ObjectId(self.relationship.object_id)},
                                                                 {"$set": {"name": relationship_id}})
        # Update vector
        vector_result = self.pick_vectors.update_one({"_id": ObjectId(self.vector.object_id)},
                                                     {"$set": {"description": vector_id}})

    # Retrieve information from database
    def get_vector(self, vector_id):
        vector_result = self.pick_vectors.find_one({"_id": ObjectId(vector_id)})
        return vector_result

    def get_node(self, node_id):
        node_result = self.pick_nodes.find_one({"_id": ObjectId(node_id)})
        return node_result

    def get_relationship(self, relation_id):
        relation_result = self.pick_relationships.find_one({"_id": ObjectId(relation_id)})
        return relation_result

    def get_event_config(self, ec_id):
        ec_result = self.pick_eventconfig.find_one({"name": ObjectId(ec_id)})
        return ec_result

    # Delete data from mongo database
    # NOTE: needs consultation with the team to determine the field through which the vector will be found
    # and deleted
    def delete_vector(self, node_id, relationship_id, vector_id, ec_id):
        # Delete node
        node_result = self.pick_nodes.delete_one({"_id": ObjectId(node_id)})
        # Delete relationship
        relationship_result = self.pick_relationships.delete_one({"_id": ObjectId(relationship_id)})
        # Delete vector
        vector_result = self.pick_vectors.delete_one({"_id": ObjectId(vector_id)})
        # Delete event config
        ec_result = self.pick_eventconfig.delete_one({"_id": ObjectId(ec_id)})

    # Serialize dictionaries (event configuration, node, relationship, vector) using JSON
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
        ec_result = self.pick_eventconfig.find_one({"_id": ObjectId(ec_id)})
        pick_collection_result = pick_datacollection.insert_one(ec_result)
        return pick_collection_result

    # Import vector collection
    # def import_vector_collection(self):
    # Connect to Lead DB
    # Get Lead vector collection
    # Save Lead vector collection in a local vector collection
