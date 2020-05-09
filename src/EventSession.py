from Vector import Vector
from Relationship import Relationship
from Node import Node
from Vector import Vector
from Connections.Database import Database
from EventConfiguration import EventConfiguration


class EventSession:
    def __init__(self, vectors=None, event_config=EventConfiguration(), selected_vector=0, log_entries=None,
                 log_files=None):
        if vectors is None:
            vectors = list()
        if log_entries is None:
            log_entries = list()
        if log_files is None:
            log_files = list()
        self.vectors = vectors
        self.event_config = event_config
        self.selected_vector = selected_vector
        self.log_entries = log_entries
        self.log_files = log_files
        pass

    def set_event_data(self, event_config, vectors):
        self.event_config = event_config
        self.vectors.clear()
        self.vectors.extend(vectors)
        self.selected_vector = 0

    def set_root_path(self, path):
        self.event_config.rootpath = path

    def set_red_team_path(self, path):
        self.event_config.redfolder = path

    def set_blue_team_path(self, path):
        self.event_config.bluefolder = path

    def set_white_team_path(self, path):
        self.event_config.whitefolder = path

    def set_event_name(self, name):
        self.event_config.name = name

    def set_event_description(self, description):
        self.event_config.description = description

    def set_start_and_end_times(self, start_time=None, end_time=None):
        if start_time is not None:
            self.event_config.starttime = start_time
        if end_time is not None:
            self.event_config.endtime = end_time

    def get_root_path(self):
        return self.event_config.rootpath

    def get_blue_team_path(self):
        return self.event_config.bluefolder

    def get_red_team_path(self):
        return self.event_config.redfolder

    def get_white_team_path(self):
        return self.event_config.whitefolder

    def get_event_name(self):
        return self.event_config.name

    def get_start_time(self):
        return self.event_config.starttime

    def get_end_time(self):
        return self.event_config.endtime

    def get_log_files(self):
        return self.log_files

    def get_log_entries(self):
        return self.log_entries

    def get_vectors(self):
        return self.vectors

    def get_selected_vector(self):
        if self.selected_vector >= len(self.vectors):
            return Vector()
        return self.vectors[self.selected_vector]

    def get_selected_nodes(self):
        if self.selected_vector >= len(self.vectors):
            return list()
        return self.vectors[self.selected_vector].get_nodes()

    def get_selected_relationships(self):
        if self.selected_vector >= len(self.vectors):
            return list()
        return self.vectors[self.selected_vector].get_relationships()

    def get_vectors_num(self):
        return len(self.vectors)

    def get_vector_at(self, num_vector):
        if 0 <= num_vector < len(self.vectors):
            return self.vectors[num_vector]

    def get_vector_list(self):
        export_list = list()
        for vector in self.vectors:
            export_list.append(vector.to_list())
        return export_list

    def get_selected_nodes_list(self):
        export_list = list()
        for node in self.get_selected_nodes():
            export_list.append(node.to_list())
        return export_list

    def get_log_entries_list(self):
        export_list = list()
        for log_entry in self.log_entries:
            export_list.append(log_entry.to_list())
        return export_list

    def select_vector(self, selection):
        if 0 <= selection < len(self.vectors):
            self.selected_vector = selection

    def add_vector(self):
        self.vectors.append(Vector(name="Vector " + str(len(self.vectors)+1)))
        print("added vector")

    def delete_vectors(self):
        to_be_deleted = []
        for i in range(len(self.vectors)):
            if self.vectors[i].is_checked_config():
                to_be_deleted.insert(0, i)

        for i in to_be_deleted:
            del self.vectors[i]

    def create_node(self):
        if len(self.vectors) == 0:
            print("No existent vector")
            return
        self.vectors[self.selected_vector].add_node()

    def add_log_entries_to_vectors(self, selected_log_entries, log_entries, selected_vectors):
        for i in selected_log_entries:
            for j in selected_vectors:
                self.vectors[j].add_node(Node.node_from_log_entry(log_entries[i]))

    def create_relationship(self, parent_id=None, child_id=None, name=""):
        if len(self.vectors) == 0:
            print("No existent vector")
            return
        parent = self.vectors[self.selected_vector].nodes[parent_id]
        child = self.vectors[self.selected_vector].nodes[child_id]
        relationship = Relationship(name=name, id=None, parent=parent, child=child)
        self.vectors[self.selected_vector].add_relationship(relationship)
