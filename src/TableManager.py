from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import *
from Vector import Vector
from Node import Node as Node
from Relationship import Relationship
from Graph import Graph as graph
import csv


class TableManager:

    def __init__(self, enforcement_action_report_table=None, log_file_table=None, log_entry_table=None,
                 node_table=None, relationship_table=None, vector_config_table=None, undo_manager=None,
                 add_to_vector_table=None, vector_drop_down=None):
        # tables
        self.enforcement_action_report_table = enforcement_action_report_table
        self.log_file_table = log_file_table
        self.log_entry_table = log_entry_table
        self.node_table = node_table
        self.relationship_table = relationship_table
        self.vector_config_table = vector_config_table
        self.add_to_vector_table = add_to_vector_table
        self.vector_drop_down = vector_drop_down

        # Misc for functionality
        self.undo_manager = undo_manager
        self.is_system_change = False
        pass

    def set_enforcement_action_report_table(self, table):
        self.enforcement_action_report_table = table

    def set_log_file_table(self, table):
        self.log_file_table = table

    def set_log_entry_table(self, table):
        self.log_entry_table = table

    def set_node_table(self, table):
        self.node_table = table

    def set_relationship_table(self, table):
        self.relationship_table = table

    def set_vector_config_table(self, table):
        self.vector_config_table = table

    # Takes a list of log entries, populates the table widget with the log entries in the list
    def populate_log_entry_table(self, log_entries):
        self.log_entry_table.setRowCount(len(log_entries))

        for i in range(len(log_entries)):
            self.log_entry_table.setRowHeight(i, 60)
            self.log_entry_table.setItem(i, 1, QTableWidgetItem(str(log_entries[i].serial)))
            self.log_entry_table.setItem(i, 2, QTableWidgetItem(log_entries[i].timestamp))
            self.log_entry_table.setItem(i, 3, QTableWidgetItem(log_entries[i].content))

            self.log_entry_table.setItem(i, 0, QTableWidgetItem(""))
            if log_entries[i].checked:
                self.log_entry_table.item(i, 0).setCheckState(QtCore.Qt.Checked)
            else:
                self.log_entry_table.item(i, 0).setCheckState(QtCore.Qt.Unchecked)

            self.log_entry_table.setItem(i, 4, QTableWidgetItem(log_entries[i].get_vector_list_str()))

    # Populates the node table given a vector index
    def populate_node_table(self, nodes):
        if self.is_system_change:
            return
        self.is_system_change = True

        self.node_table.setRowCount(len(nodes))
        for i in range(len(nodes)):
            self.node_table.setItem(i, 0, QTableWidgetItem(nodes[i].get_id()))
            self.node_table.setItem(i, 1, QTableWidgetItem(nodes[i].name))
            self.node_table.setItem(i, 2, QTableWidgetItem(nodes[i].get_timestamp()))
            self.node_table.setItem(i, 3, QTableWidgetItem(nodes[i].description))
            self.node_table.setItem(i, 4, QTableWidgetItem(nodes[i].get_reference()))
            self.node_table.setItem(i, 5, QTableWidgetItem(nodes[i].log_creator))
            self.node_table.setItem(i, 6, QTableWidgetItem(nodes[i].event_type))
            self.node_table.setItem(i, 7, QTableWidgetItem(nodes[i].icon_type))
            self.node_table.setItem(i, 8, QTableWidgetItem(nodes[i].source))

            self.node_table.setItem(i, 9, QTableWidgetItem(""))
            if nodes[i].is_visible():
                self.node_table.item(i, 9).setCheckState(QtCore.Qt.Checked)
            else:
                self.node_table.item(i, 9).setCheckState(QtCore.Qt.Unchecked)
        self.is_system_change = False

    # Populates the vector configuration table with the vectors
    def populate_vector_configuration_table(self, vectors):
        self.vector_config_table.setRowCount(len(vectors))
        for i in range(len(vectors)):
            item = QTableWidgetItem("")

            if vectors[i].is_checked_config():
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.vector_config_table.setItem(i, 0, item)
            self.vector_config_table.setItem(i, 1, QTableWidgetItem(vectors[i].name))
            self.vector_config_table.setItem(i, 2, QTableWidgetItem(vectors[i].description))

    # Populate the relationship table given a vector index
    def populate_relationship_table(self, relationships):
        self.relationship_table.setRowCount(len(relationships))
        for i in range(len(relationships)):
            self.relationship_table.setItem(i, 0, QTableWidgetItem(relationships[i].get_id_str()))
            self.relationship_table.setItem(i, 1, QTableWidgetItem(relationships[i].get_name()))
            self.relationship_table.setItem(i, 2, QTableWidgetItem(relationships[i].get_parent_id()))
            self.relationship_table.setItem(i, 3, QTableWidgetItem(relationships[i].get_child_id()))

    # Populates the selected combo_box with the vector names
    def populate_vector_dropdowns(self, vectors):
        self.vector_drop_down.clear()
        for i in range(len(vectors)):
            self.vector_drop_down.addItem(vectors[i].name)

    # Populates the selected combo_box with the node names
    def populate_node_dropdowns(self, combo_box, nodes):
        combo_box.clear()
        for i in range(len(nodes)):
            combo_box.addItem(nodes[i].name)

    def populate_add_to_vector_table(self, vectors):
        self.add_to_vector_table.setRowCount(len(vectors))
        for i in range(len(vectors)):
            self.add_to_vector_table.setItem(i, 0, QTableWidgetItem(vectors[i].name))
            if vectors[i].is_checked_add_log_entry():
                self.add_to_vector_table.item(i, 0).setCheckState(QtCore.Qt.Checked)
            else:
                self.add_to_vector_table.item(i, 0).setCheckState(QtCore.Qt.Unchecked)

    def populate_log_file_table(self, log_files):
        self.log_file_table.setRowCount(len(log_files))
        for i in range(len(log_files)):
            self.log_file_table.setItem(i, 0, QTableWidgetItem(log_files[i].name))
            self.log_file_table.setItem(i, 1, QTableWidgetItem(log_files[i].path))
            self.log_file_table.setItem(i, 2, QTableWidgetItem("Cleansed"))
            self.log_file_table.setItem(i, 3, QTableWidgetItem(log_files[i].get_validation_status()))
            self.log_file_table.setItem(i, 4, QTableWidgetItem(log_files[i].get_ingestion_status()))
            self.log_file_table.setItem(i, 5, QTableWidgetItem(""))

            if log_files[i].is_marked():
                self.log_file_table.item(i, 5).setCheckState(QtCore.Qt.Checked)
            else:
                self.log_file_table.item(i, 5).setCheckState(QtCore.Qt.Unchecked)

    def populate_enforcement_action_report_table(self, log_file):
        self.enforcement_action_report_table.setRowCount(len(log_file.errors))
        for i in range(len(log_file.errors)):
            self.enforcement_action_report_table.setItem(i, 0, QTableWidgetItem(str(log_file.errors[i][0])))
            self.enforcement_action_report_table.setItem(i, 1, QTableWidgetItem(log_file.errors[i][1]))

    def edit_node_table(self, row, column, value, nodes, from_undo=False):
        if self.is_system_change:
            return
        print("editing node and is system changes is: ", self.is_system_change)
        undo_val = ""
        special_command = False
        if column == 9:
            undo_val = nodes[row].visibility
            nodes[row].visibility = value
        elif column == 1:
            undo_val = nodes[row].name
            nodes[row].name = value
        elif column == 3:
            undo_val = nodes[row].description
            nodes[row].description = value
        elif column == 5:
            undo_val = nodes[row].log_creator
            nodes[row].set_log_creator(value)
            special_command = True

        if not self.is_system_change and not from_undo:
            self.undo_manager.add_command("set_node_field", [row, column, undo_val])
        return

    def edit_vector_table(self, row, column, value, vectors):
        if column == 0:
            vectors[row].checked_configuration_table = value
        elif column == 1:
            vectors[row].name = value
        elif column == 2:
            vectors[row].description = value
        return

    def export_table(self, export_list, filename="Output.csv"):
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(export_list)
