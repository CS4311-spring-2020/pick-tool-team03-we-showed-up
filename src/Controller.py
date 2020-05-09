from EventSession import EventSession
from TableManager import TableManager
from MainUI import UIMain
from SPLUNKInterface import SPLUNKInterface
from IngestionManager import IngestionManager
from Graph import GraphInterface
from Connections.Database import Database

class Controller:
    def __init__(self, event_session=None, table_manager=None, splunk=None,
                 ingestion=None, view=None, graph=None, db=None):
        self.event_session = event_session
        self.table_manager = table_manager
        self.splunk = splunk
        self.ingestion = ingestion
        self.view = view
        self.graph = graph
        self.db = db
        pass

    def set_event_name(self, name):
        self.event_session.set_event_name = name

    def set_display_vector(self, v_num):
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.event_session.select_vector(v_num)
        self.graph.set_vector(self.event_session.get_selected_vector())

    def update_node_and_relationship_tables(self):
        self.update_node_table()
        self.update_relationship_table()

    def update_node_table(self):
        nodes = self.event_session.get_selected_nodes()
        self.table_manager.populate_node_table(nodes)

    def update_log_entry_table(self):
        try:
            self.event_session.log_entries = self.splunk.get_entries()
        except Exception as e:
            print(e)
        self.table_manager.populate_log_entry_table(self.event_session.get_log_entries())

    def update_vector_tables(self):
        vectors = self.event_session.get_vectors()
        self.table_manager.populate_vector_configuration_table(vectors)
        self.table_manager.populate_add_to_vector_table(vectors)

    def update_relationship_table(self):
        relationships = self.event_session.get_selected_relationships()
        self.table_manager.populate_relationship_table(relationships)

    def update_vector_dropdwon(self):
        vectors = self.event_session.get_vectors()
        self.table_manager.populate_vector_dropdowns(vectors)

    def update_node_dropdowns(self, combo_box):
        nodes = self.event_session.get_selected_nodes()
        self.table_manager.populate_node_dropdowns(combo_box, nodes)

    def update_folder_path(self, team, path):
        if team == "root":
            self.event_session.set_root_path(str(path))
        elif team == "red":
            self.event_session.set_red_team_path(str(path))
        elif team == "blue":
            self.event_session.set_blue_team_path(str(path))
        elif team == "white":
            self.event_session.set_white_team_path(str(path))

    # Called once the start ingestion button is clicked, it sends the user input for folder paths
    def start_ingestion(self):
        event_name = self.event_session.get_event_name()
        root_path = self.event_session.get_root_path()
        red_folder = self.event_session.get_red_team_path()
        blue_folder = self.event_session.get_blue_team_path()
        white_folder = self.event_session.get_white_team_path()

        self.ingestion.ingest_directory_to_splunk(root_path, event_name, self.splunk)

        if red_folder == "":
            red_folder = root_path + "/red"
            self.event_session.set_red_team_path(red_folder)
        self.ingestion.ingest_directory_to_splunk(red_folder, event_name, self.splunk)

        if blue_folder == "":
            blue_folder = root_path + "/blue"
            self.event_session.set_blue_team_path(blue_folder)
        self.ingestion.ingest_directory_to_splunk(blue_folder, event_name, self.splunk)

        if white_folder == "":
            white_folder = root_path + "/white"
            self.event_session.set_white_team_path(white_folder)
        self.ingestion.ingest_directory_to_splunk(white_folder, event_name, self.splunk)

    def update_event_data(self, object_id):
        event_map = self.db.get_event_data(object_id)
        self.event_session.set_event_data(event_map["event_config"], event_map["vectors"])
        self.update_node_and_relationship_tables()
        self.update_vector_tables()
        self.update_vector_dropdwon()

    def update_event_db(self):
        self.db.update_event(self.event_session.event_config, self.event_session.get_vectors())

    def update_splunk_filter(self, keyword, start_time=None, end_time=None):
        print("Splunk filtering to keyword: ", keyword)
        self.splunk.set_keyword(keyword)

        # print("Earliest time is: ", start_time.toPyDateTime().timestamp())
        # self.splunk.set_earliest_time(start_time.toString("dd/MM/yyyy:hh:mm:ss"))

        self.splunk.get_log_count(bypass_check=True)
        self.table_manager.populate_log_entry_table(self.event_session.get_log_entries())

    def add_vector(self):
        self.event_session.add_vector()
        self.update_vector_tables()
        self.update_node_and_relationship_tables()
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.graph.set_vector(self.event_session.get_selected_vector())

    def delete_vector(self):
        self.event_session.delete_vectors()
        vectors = self.event_session.get_vectors()
        self.table_manager.populate_vector_configuration_table(vectors)
        self.table_manager.populate_add_to_vector_table(vectors)
        self.table_manager.populate_vector_dropdowns(vectors)
        self.update_node_and_relationship_tables()
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.graph.set_vector(self.event_session.get_selected_vector())

    # TODO: Add relationship method
    def create_node(self):
        if len(self.event_session.get_vectors()) == 0:
            return
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.event_session.create_node()
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.graph.set_vector(self.event_session.get_selected_vector())
        self.update_node_and_relationship_tables()

    def create_relationship(self, parent_id, child_id, name):
        if len(self.event_session.get_vectors()) == 0:
            return
        self.event_session.create_relationship(parent_id, child_id, name)
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.graph.set_vector(self.event_session.get_selected_vector())
        self.update_node_and_relationship_tables()

    def add_log_entry_to_vector(self, selected_log_entries, selected_vectors):
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.event_session.add_log_entries_to_vectors(selected_log_entries, self.event_session.get_log_entries(),
                                                      selected_vectors)
        pass

    def validate_anyway_clicked(self):
        event_name = self.event_session.get_event_name()
        self.ingestion.validate_file_anyway(event_name, self.splunk)

    def create_event(self, name, description, start_time, end_time):
        flag = self.splunk.createEvent(name)
        if (not flag == 1) and (not flag == 2) and (not flag == 3):
            self.event_session.set_event_name(name)
            self.event_session.set_event_description(description)
            self.event_session.set_start_and_end_times(start_time=start_time, end_time=end_time)
        return flag

    def edit_node_table(self, row, column, value):
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.table_manager.edit_node_table(row, column, value, self.event_session.get_selected_nodes())
        self.update_node_and_relationship_tables()
        self.graph.set_vector(self.event_session.get_selected_vector())

    def edit_vector_configuration_table(self, row, column, value):
        self.table_manager.edit_vector_table(row, column,value, self.event_session.get_vectors())

    def export_log_entry_table(self, filename):
        export_list = self.event_session.get_log_entries_list()
        self.table_manager.export_table(export_list, filename=filename)

    def export_node_table(self, filename):
        export_list = self.event_session.get_selected_nodes_list()
        self.table_manager.export_table(export_list, filename=filename)

    def export_vector_configuration_table(self, filename):
        export_list = self.event_session.get_vector_list()
        self.table_manager.export_table(export_list, filename=filename)