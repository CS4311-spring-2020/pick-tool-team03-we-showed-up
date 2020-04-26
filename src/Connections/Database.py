from EventConfiguration import EventConfiguration
from Node import Node
from Relationship import Relationship
from Vector import Vector

from pymongo import MongoClient

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
        self.vector = Vector();

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
        print(ec_result)
        # Insert node dictionary
        node_result = self.pick_nodes.insert_one(self.node_dictionary)
        print(node_result)
        # Insert relationship dictionary
        relationship_result = self.pick_relationships.insert_one(self.relationship_dictionary)
        print(relationship_result)
        # Insert vector dictionary
        vector_result = self.pick_vectors.insert_one(self.vector_dictionary)
        print(vector_result)

    # Update data from mongo database
    # NOTE: needs consultation with the team since multiple items in the vector can be updated
    def update_vector(self, update_item):
        # Update event config
        ec_result = self.pick_eventconfig.update_one({"name": self.ec_dictionary['name']}, {"$set": {"name": update_item}})
        # Update node
        node_result = self.pick_nodes.update_one({"id": self.node_dictionary['id']},
                                                     {"$set": {"name": update_item}})
        # Update relationship
        relationship_result = self.pick_relationships.update_one({"id": self.relationship_dictionary['id']},
                                                 {"$set": {"name": update_item}})
        # Update vector
        vector_result = self.pick_vectors.update_one({"name": self.vector_dictionary['name']},
                                                                 {"$set": {"description": update_item}})

    # Delete data from mongo database
    # NOTE: needs consultation with the team to determine the field through which the vector will be found
    # and deleted
    def delete_vector(self, delete_item):
        # Delete event config
        ec_result = self.pick_eventconfig.delete_one({"name": self.ec_dictionary['name']})
        # Delete node
        node_result = self.pick_nodes.delete_one({"id": self.node_dictionary['id']})
        # Delete relationship
        relationship_result = self.pick_relationships.delete_one({"id": self.relationship_dictionary['id']})
        # Delete vector
        vector_result = self.pick_vectors.delete_one({"name": self.vector_dictionary['name']})

    # Export vector collection
    def export_vector_collection(self):
        # Export vector collection (this is not how you do it though...)
        pick_datacollection = self.pick_database['pick_collection']
        pick_collection_result = pick_datacollection.insert_many([self.pick_eventconfig, self.pick_nodes,
                                                                  self.pick_relationships, self.pick_vectors])
        return pick_collection_result

    # Import vector collection
    #def import_vector_collection(self):
        # Connect to Lead DB
        # Get Lead vector collection
        # Save Lead vector collection in a local vector collection