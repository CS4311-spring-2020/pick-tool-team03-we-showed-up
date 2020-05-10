from Node import Node
from Vector import  Vector
from Relationship import Relationship
from EventConfiguration import EventConfiguration
from Connections.Database import Database
from time import  sleep

class dataRetrievalTest:
    """Simple class to test the persistence of the data of an event and retrieval."""
    if __name__ == "__main__":
        db = Database()
        event_map = db.get_event_map()
        out_map = db.get_event_data(event_map['changed_name_7'])
        print(out_map.keys())
        vectors = out_map['vectors']
        ec = out_map['event_config']
        ec.name = "changed_name_7"
        counter = 0
        for v in vectors:
            v.name = "vector" + str(counter)
            v.add_node()
            # print(v.get_nodes())
            counter += 1

        db.update_event(ec, vectors)