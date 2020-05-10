class Controller:
    def __init__(self, event_session=None, table_manager=None, splunk=None,
                 ingestion=None, view=None, graph=None, db=None, undo_manager=None):
        self.event_session = event_session
        self.table_manager = table_manager
        self.splunk = splunk
        self.ingestion = ingestion
        self.view = view
        self.graph = graph
        self.db = db
        self.undo_manager = undo_manager
        if self.splunk is not None:
            print("connected splunk signal")
            self.splunk.updated_entries.connect(self.update_log_entry_table)
        pass
        if undo_manager is not None:
            print("connected undo manager signal")
            self.undo_manager.updated_nodes.connect(self.update_node_and_relationship_tables)

    def set_event_name(self, name):
        """Sets the event name into the event session sata."""
        self.event_session.set_event_name = name

    def set_display_vector(self, v_num):
        """Sets the vector to be displayed into the event session data."""
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.event_session.select_vector(v_num)
        self.graph.set_vector(self.event_session.get_selected_vector())

    def update_node_and_relationship_tables(self):
        """Updates the node and relationship tables using the table manager."""
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.update_node_table()
        self.update_relationship_table()
        self.graph.set_vector(self.event_session.get_selected_vector())

    def update_node_table(self):
        """Update the node table using the table manager and saves the state of the graph."""
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        nodes = self.event_session.get_selected_nodes()
        self.table_manager.populate_node_table(nodes)
        self.graph.set_vector(self.event_session.get_selected_vector())

    def update_log_entry_table(self):
        """Gathers the new the log entries from SPLUNK and updates the log entry table."""
        try:
            self.event_session.log_entries = self.splunk.get_entries()
        except Exception as e:
            print(e)
        self.table_manager.populate_log_entry_table(self.event_session.get_log_entries())

    def update_vector_tables(self):
        """Updates the vector configuration table and the add-to-vector table."""
        vectors = self.event_session.get_vectors()
        self.table_manager.populate_vector_configuration_table(vectors)
        self.table_manager.populate_add_to_vector_table(vectors)

    def update_relationship_table(self):
        """Updates the relationship table using the table manager"""
        relationships = self.event_session.get_selected_relationships()
        self.table_manager.populate_relationship_table(relationships)

    def update_vector_dropdwon(self):
        """Updates the vector dropdown using the table manager."""
        vectors = self.event_session.get_vectors()
        self.table_manager.populate_vector_dropdowns(vectors)

    def update_node_dropdowns(self, combo_box):
        """Takes a combo box from the parameter and updates it with the vector names by using the table manager."""
        nodes = self.event_session.get_selected_nodes()
        self.table_manager.populate_node_dropdowns(combo_box, nodes)

    def update_folder_path(self, team, path):
        """Sets the path in the event session corresponding to the team key"""
        if team == "root":
            self.event_session.set_root_path(str(path))
        elif team == "red":
            self.event_session.set_red_team_path(str(path))
        elif team == "blue":
            self.event_session.set_blue_team_path(str(path))
        elif team == "white":
            self.event_session.set_white_team_path(str(path))

    def start_ingestion(self):
        """Calls the ingestion process to start."""
        self.ingestion.start_ingestion()

    def update_event_data(self, object_id):
        """Updates the event data corresponding to the id, from the one stored in the database."""
        event_map = self.db.get_event_data(object_id)
        self.event_session.set_event_data(event_map["event_config"], event_map["vectors"])
        self.update_node_and_relationship_tables()
        self.update_vector_tables()
        self.update_vector_dropdwon()

    def update_event_db(self):
        """Updates the database with the event session data."""
        self.db.update_event(self.event_session.event_config, self.event_session.get_vectors())

    def update_splunk_filter(self, keyword, start_time=None, end_time=None):
        """Updates the Splunk filter with a keyword, start and end times. """
        print("Splunk filtering to keyword: ", keyword)
        self.splunk.set_keyword(keyword)

        # print("Earliest time is: ", start_time.toPyDateTime().timestamp())
        # self.splunk.set_earliest_time(start_time.toString("dd/MM/yyyy:hh:mm:ss"))

        self.splunk.update_entries(bypass_check=True)
        self.table_manager.populate_log_entry_table(self.event_session.get_log_entries())

    def add_vector(self):
        """Adds a vector to the event session."""
        self.event_session.add_vector()
        self.update_vector_tables()
        self.update_node_and_relationship_tables()
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.graph.set_vector(self.event_session.get_selected_vector())

    def delete_vector(self):
        """Deletes the selected vectors from the event session."""
        self.event_session.delete_vectors()
        vectors = self.event_session.get_vectors()
        self.table_manager.populate_vector_configuration_table(vectors)
        self.table_manager.populate_add_to_vector_table(vectors)
        self.table_manager.populate_vector_dropdowns(vectors)
        self.update_node_and_relationship_tables()
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.graph.set_vector(self.event_session.get_selected_vector())

    def create_node(self):
        """Creates a blank node inside the selected vector, if any."""
        if len(self.event_session.get_vectors()) == 0:
            return
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.event_session.create_node()
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.graph.set_vector(self.event_session.get_selected_vector())
        self.update_node_and_relationship_tables()

    def create_relationship(self, parent_id, child_id, name):
        """Creates a relationship inside the selected vector, if any. References the parent and child nodes
        corresponding to the passed IDs."""
        if len(self.event_session.get_vectors()) == 0:
            return
        self.event_session.create_relationship(parent_id, child_id, name)
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.graph.set_vector(self.event_session.get_selected_vector())
        self.update_node_and_relationship_tables()

    def add_log_entry_to_vector(self, selected_log_entries, selected_vectors):
        """Adds the selected log entries as vectors into the selected vectors."""
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.event_session.add_log_entries_to_vectors(selected_log_entries, self.event_session.get_log_entries(),
                                                      selected_vectors)
        pass

    def validate_anyway_clicked(self):
        """Bypasses validation for the selected log file."""
        event_name = self.event_session.get_event_name()
        self.ingestion.validate_file_anyway(event_name, self.splunk)

    def create_event(self, name, description, start_time, end_time):
        """Creates a new event given the name, description, start and end time."""
        flag = self.splunk.createEvent(name)
        if (not flag == 1) and (not flag == 2) and (not flag == 3):
            self.event_session.set_event_name(name)
            self.event_session.set_event_description(description)
            self.event_session.set_start_and_end_times(start_time=start_time, end_time=end_time)
        return flag

    def edit_node_table(self, row, column, value):
        """Triggered when the node table is clicked, it will update the corresponding field of the node
        and update the tables an graph."""
        self.graph.save_node_positions(self.event_session.get_selected_vector())
        self.table_manager.edit_node_table(row, column, value, self.event_session.get_selected_nodes())
        self.update_node_and_relationship_tables()
        self.graph.set_vector(self.event_session.get_selected_vector())

    def edit_vector_configuration_table(self, row, column, value):
        """Triggered when the vc table is clicked, it will update the corresponding field of the vector
        and update the table."""
        self.table_manager.edit_vector_table(row, column,value, self.event_session.get_vectors())

    def export_log_entry_table(self, filename):
        """Export log entry table into a csv with the filename."""
        export_list = self.event_session.get_log_entries_list()
        self.table_manager.export_table(export_list, filename=filename)

    def export_node_table(self, filename):
        """Export node table into a csv with the filename."""
        export_list = self.event_session.get_selected_nodes_list()
        self.table_manager.export_table(export_list, filename=filename)

    def export_vector_configuration_table(self, filename):
        """Export vector configuration table into a csv with the filename."""
        export_list = self.event_session.get_vector_list()
        self.table_manager.export_table(export_list, filename=filename)

    def connect_to_splunk(self, username, password):
        """Connects the client to SPLUNK with the given credential, returns True if the connection was
        successful and False otherwise."""
        try:
            self.splunk.connect_client(username=username, password=password)
            return True
        except Exception as e:
            print(e)
            return False
