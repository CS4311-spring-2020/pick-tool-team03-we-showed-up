from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import *
from Vector import Vector
from Node import Node as Node
from Relationship import Relationship
from graph import graph as graph
import csv


class TableManager:

    def __init__(self, enforcement_action_report_table=None, log_file_table=None, log_entry_table=None,
                 node_table=None, relationship_table=None, vector_config_table=None, log_entries=[], vectors=[],
                 undo_manager=None):
        self.enforcement_action_report_table = enforcement_action_report_table
        self.log_file_table = log_file_table
        self.log_entry_table = log_entry_table
        self.node_table = node_table
        self.relationship_table = relationship_table
        self.vector_config_table = vector_config_table
        self.vectors = vectors
        self.log_entries = log_entries
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
    def populate_logentry_table(self, logentries):
        self.log_entries = logentries

        self.log_entry_table.setRowCount(len(logentries))

        for i in range(len(logentries)):
            self.log_entry_table.setRowHeight(i, 60)
            self.log_entry_table.setItem(i, 1, QTableWidgetItem(str(logentries[i].serial)))
            self.log_entry_table.setItem(i, 2, QTableWidgetItem(logentries[i].timestamp))
            self.log_entry_table.setItem(i, 3, QTableWidgetItem(logentries[i].content))

            self.log_entry_table.setItem(i, 0, QTableWidgetItem(""))
            if logentries[i].checked:
                self.log_entry_table.item(i, 0).setCheckState(QtCore.Qt.Checked)
            else:
                self.log_entry_table.item(i, 0).setCheckState(QtCore.Qt.Unchecked)

            self.log_entry_table.setItem(i, 4, QTableWidgetItem(logentries[i].get_vector_list_str()))

    # Populates the node table given a vector index
    def populate_node_table(self, vector_num):
        if self.is_system_change:
            return
        self.is_system_change = True
        if len(self.vectors) == 0 or vector_num < 0 or vector_num >= len(self.vectors):
            self.is_system_change = False
            return

        self.node_table.setRowCount(len(self.vectors[vector_num].get_nodes()))
        for i in range(len(self.vectors[vector_num].get_nodes())):
            self.node_table.setItem(i, 0, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].get_id()))
            self.node_table.setItem(i, 1, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].name))
            self.node_table.setItem(i, 2, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].get_timestamp()))
            self.node_table.setItem(i, 3, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].description))
            self.node_table.setItem(i, 4, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].get_reference()))
            self.node_table.setItem(i, 5, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].log_creator))
            self.node_table.setItem(i, 6, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].event_type))
            self.node_table.setItem(i, 7, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].icon_type))
            self.node_table.setItem(i, 8, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].source))

            self.node_table.setItem(i, 9, QTableWidgetItem(""))
            if self.vectors[vector_num].get_nodes()[i].is_visible():
                self.node_table.item(i, 9).setCheckState(QtCore.Qt.Checked)
            else:
                self.node_table.item(i, 9).setCheckState(QtCore.Qt.Unchecked)
        self.is_system_change = False

    # Populates the vector configuration table with the vectors
    def populate_vector_configuration_table(self):
        self.vector_config_table.setRowCount(len(self.vectors))

        for i in range(len(self.vectors)):
            self.vector_config_table.setItem(i, 0, QTableWidgetItem(""))
            if self.vectors[i].is_checked_config():
                self.vector_config_table.item(i, 0).setCheckState(QtCore.Qt.Checked)
            else:
                self.vector_config_table.item(i, 0).setCheckState(QtCore.Qt.Unchecked)

            self.vector_config_table.setItem(i, 1, QTableWidgetItem(self.vectors[i].name))
            self.vector_config_table.setItem(i, 2, QTableWidgetItem(self.vectors[i].description))

    # Populate the relationship table given a vector index
    def populate_relationship_table(self, vector_num):
        print('called populate relationship table from vector: ', vector_num)
        if len(self.vectors) == 0 or vector_num < 0 or vector_num >= len(self.vectors):
            return

        self.relationship_table.setRowCount(len(self.vectors[vector_num].get_relationships()))
        for i in range(len(self.vectors[vector_num].get_relationships())):
            print(self.vectors[vector_num].get_relationships()[i].get_name())
            self.relationship_table.setItem(i, 0, QTableWidgetItem(self.vectors[vector_num].get_relationships()[i].
                                                                   get_id_str()))
            self.relationship_table.setItem(i, 1, QTableWidgetItem(self.vectors[vector_num].get_relationships()[i].
                                                                   get_name()))
            self.relationship_table.setItem(i, 2, QTableWidgetItem(self.vectors[vector_num].get_relationships()[i].
                                                                   get_parent_id()))
            self.relationship_table.setItem(i, 3, QTableWidgetItem(self.vectors[vector_num].get_relationships()[i].
                                                                   get_child_id()))

    def populate_vector_dropdowns(self, combo_box):
        combo_box.clear()

        for i in range(len(self.vectors)):
            combo_box.addItem(self.vectors[i].name)

    def populate_node_dropdowns(self, selected_vector, combo_box):
        combo_box.clear()

        for i in range(len(self.vectors[selected_vector].nodes)):
            combo_box.addItem(self.vectors[selected_vector].nodes[i].name)

    def populate_add_to_vector_table(self, table_widget):
        table_widget.setRowCount(len(self.vectors))
        for i in range(len(self.vectors)):
            table_widget.setItem(i, 0, QTableWidgetItem(self.vectors[i].name))
            if self.vectors[i].is_checked_add_log_entry():
                table_widget.item(i, 0).setCheckState(QtCore.Qt.Checked)
            else:
                table_widget.item(i, 0).setCheckState(QtCore.Qt.Unchecked)

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

    def create_node(self, vector_num):
        if len(self.vectors) == 0:
            print("No existent vector")
            return
        self.vectors[vector_num].add_node()

    def create_relationship(self, vector_num, parent_id=None, child_id=None, name=""):
        if len(self.vectors) == 0:
            print("No existent vector")
            return
        parent = self.vectors[vector_num].nodes[parent_id]
        child = self.vectors[vector_num].nodes[child_id]
        relationship = Relationship(name=name, id=None, parent=parent, child=child)
        self.vectors[vector_num].add_relationship(relationship)

    def edit_node_table(self, row, column, value, vector_num, from_undo=False):
        if self.is_system_change:
            return
        print("editing node and is system changes is: ", self.is_system_change)
        undo_val = ""
        special_command = False
        if column == 9:
            undo_val = self.vectors[vector_num].nodes[row].visibility
            self.vectors[vector_num].nodes[row].visibility = value
        elif column == 1:
            undo_val = self.vectors[vector_num].nodes[row].name
            self.vectors[vector_num].nodes[row].name = value
        elif column == 3:
            undo_val = self.vectors[vector_num].nodes[row].description
            self.vectors[vector_num].nodes[row].description = value
        elif column == 5:
            undo_val = self.vectors[vector_num].nodes[row].log_creator
            self.vectors[vector_num].nodes[row].set_log_creator(value)
            special_command = True

        if not self.is_system_change and not from_undo:
            self.undo_manager.add_command("set_node_field", [row, column, undo_val, vector_num])
        if from_undo:
            self.populate_node_table(vector_num)

        if special_command:
            self.populate_node_table(vector_num)
        return

    def edit_vector_table(self, row, column, value):
        if column == 0:
            self.vectors[row].checked_configuration_table = value
        elif column == 1:
            self.vectors[row].name = value
        elif column == 2:
            self.vectors[row].description = value
        return

    # def export_table_to_csv(self, table_widget, filename="output.csv"):
    #     export_list = list()
    #
    #     for i in range(table_widget.rowCount()):
    #         temp_list = list()
    #         print("Current row is: ", i)
    #         for j in range(table_widget.columnCount()):
    #             temp_list.append(table_widget.itemAt(j, i).text())
    #             print("    col: ", j, " item is: ", table_widget.itemAt(j, i).text())
    #         export_list.append(temp_list)
    #
    #     with open(filename, "w") as f:
    #         writer = csv.writer(f)
    #         writer.writerows(export_list)

    def export_log_entry_table(self, filename="Log Entry Table Output.csv"):
        export_list = list()
        for log_entry in self.log_entries:
            export_list.append(log_entry.to_list())
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(export_list)

    def export_node_table(self, vector_num, filename="Node Table Output.csv"):
        export_list = list()
        print("Exporting nodes in vector: ", vector_num)
        for node in self.vectors[vector_num].get_nodes():
            export_list.append(node.to_list())
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(export_list)

    def export_vector_configuration_table(self, filename="Vector Configuration Table Output.csv"):
        export_list = list()
        for vector in self.vectors:
            export_list.append(vector.to_list())
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(export_list)

    def add_log_entries_to_vectors(self, selected_log_entries, log_entries, selected_vectors):
        for i in selected_log_entries:
            for j in selected_vectors:
                self.vectors[j].add_node(Node.node_from_log_entry(log_entries[i]))
                # graph.set_vector(self.vectors[j])

    def populate_all_tables(self):
        self.populate_relationship_table(0)
        self.populate_node_table(0)
        self.populate_vector_configuration_table()
