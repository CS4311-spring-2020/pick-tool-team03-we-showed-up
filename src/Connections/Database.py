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
    def insert_vector(self):
        # Insert data to mongodb
        # Insert event configuration dictionary
        ec_result = self.pick_eventconfig.insert_one(self.ec_dictionary)
        print(ec_result.inserted_id)
        ec_id = ec_result.inserted_id
        self.ec.set_object_id(str(ec_id))
        # self.ec.set_object_id(self.get_event_config_id)

        # Insert node dictionary
        node_result = self.pick_nodes.insert_one(self.node_dictionary)
        print(node_result.inserted_id)
        node_id = node_result.inserted_id
        self.node.set_object_id(str(node_id))
        # self.node.set_object_id(self.get_node_id())

        # Insert relationship dictionary
        relationship_result = self.pick_relationships.insert_one(self.relationship_dictionary)
        print(relationship_result.inserted_id)
        relationship_id = relationship_result.inserted_id
        self.relationship.set_object_id(str(relationship_id))
        # self.relationship.set_object_id(self.get_relationship_id())

        # Insert vector dictionary
        vector_result = self.pick_vectors.insert_one(self.vector_dictionary)
        print(vector_result.inserted_id)
        vector_id = vector_result.inserted_id
        self.vector.set_object_id(str(vector_id))
        # self.vector.set_object_id(self.get_vector_id())

    # Update data from mongo database
    # NOTE: needs consultation with the team since multiple items in the vector can be updated
    def update_vector(self, update_item):
        # Update event config
        # NOTE: for update and delete, we take the object_id directly from the objects rather than the dictionary
        ec_result = self.pick_eventconfig.update_one({"_id": ObjectId(self.ec.object_id)},
                                                     {"$set": {"name": update_item}})
        # Update node
        node_result = self.pick_nodes.update_one({"_id": ObjectId(self.node.object_id)},
                                                 {"$set": {"name": update_item}})
        # Update relationship
        relationship_result = self.pick_relationships.update_one({"_id": ObjectId(self.relationship.object_id)},
                                                                 {"$set": {"name": update_item}})
        # Update vector
        vector_result = self.pick_vectors.update_one({"_id": ObjectId(self.vector.object_id)},
                                                     {"$set": {"description": update_item}})

    # Retrieve information from database
    def get_vector(self, vector_item):
        vector_result = self.pick_vectors.find_one({"_id": ObjectId(self.vector.object_id)})
        return vector_result

    def get_node(self, node_item):
        node_result = self.pick_nodes.find_one({"_id": ObjectId(self.node.object_id)})
        return node_result

    def get_relationship(self, relation_item):
        relation_result = self.pick_relationships.find_one({"_id": ObjectId(self.relationship.object_id)})
        return relation_result

    def get_event_config(self, ec_item):
        ec_result = self.pick_eventconfig.find_one({"name": ObjectId(self.ec.object_id)})
        item = ec_result.get(ec_item)
        return item

    # Delete data from mongo database
    # NOTE: needs consultation with the team to determine the field through which the vector will be found
    # and deleted
    def delete_vector(self, delete_item):
        # Delete event config
        ec_result = self.pick_eventconfig.delete_one({"_id": ObjectId(self.ec.object_id)})
        # Delete node
        node_result = self.pick_nodes.delete_one({"_id": ObjectId(self.node.object_id)})
        # Delete relationship
        relationship_result = self.pick_relationships.delete_one({"_id": ObjectId(self.relationship.object_id)})
        # Delete vector
        vector_result = self.pick_vectors.delete_one({"_id": ObjectId(self.vector.object_id)})

    # Serialize dictionaries (event configuration, node, relationship, vector) using JSON
    def serialize_eventconfig(self, dictionary):
        temp_ec_dictionary = self.ec_dictionary
        app_json = dumps(temp_ec_dictionary)
        print(app_json)
        return app_json

    def serialize_node(self, dictionary):
        temp_node_dictionary = self.node_dictionary
        app_json = dumps(temp_node_dictionary)
        print(app_json)
        return app_json

    def serialize_relationship(self, item):
        temp_relationship_dictionary = self.relationship_dictionary
        app_json = dumps(temp_relationship_dictionary)
        print(app_json)
        return app_json

    def serialize_vector(self, item):
        temp_vector_dictionary = self.vector_dictionary
        app_json = dumps(temp_vector_dictionary)
        print(app_json)
        return app_json

    # Deserialize dictionaries (event configuration, node, relationship, vector) using JSON
    def deserialize_eventconfig(self, dictionary):
        decoded_ec_dictionary = self.ec_dictionary
        decode_json_ec = loads(decoded_ec_dictionary)
        print(decode_json_ec)
        return decode_json_ec

    def deserialize_node(self, dictionary):
        decoded_node_dictionary = self.node_dictionary
        decode_json_node = loads(decoded_node_dictionary)
        print(decode_json_node)
        return decode_json_node

    def deserialize_relationship(self, item):
        decoded_relationship_dictionary = self.relationship_dictionary
        decode_json_rel = loads(decoded_relationship_dictionary)
        print(decode_json_rel)
        return decode_json_rel

    def deserialize_vector(self, item):
        decode_vector_dictionary = self.vector_dictionary
        decode_json_vec = loads(decode_vector_dictionary)
        print(decode_json_vec)
        return decode_json_vec

    # Export vector collection
    def export_vector_collection(self):
        # Export vector collection (this is not how you do it though...)
        pick_datacollection = self.pick_database['pick_collection']
        pick_collection_result = pick_datacollection.insert_one([{self.pick_eventconfig, self.pick_nodes,
                                                                  self.pick_relationships, self.pick_vectors}])
        return pick_collection_result

    # Import vector collection
    # def import_vector_collection(self):
    # Connect to Lead DB
    # Get Lead vector collection
    # Save Lead vector collection in a local vector collection
