from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import math
from demo_data import DemoData
from random import randint
from Vector import Vector
from Node import Node as Node
from Relationship import Relationship
import csv


class manage_tables:
    enforcement_action_report_table = None
    log_file_table = None

    def __init__(self, enforcement_action_report_table=None, log_file_table=None):
        self.enforcement_action_report_table = enforcement_action_report_table
        self.log_file_table = log_file_table
        self.vectors = []
        pass


    def add_enforcement_action_report_table(self, table):
        self.enforcement_action_report_table = table

    def add_log_file_table(self, table):
        self.log_file_table = table

    def populate_lfc_table(self, table_widget):
        table_widget.setRowCount(len(self.log_file))
        for i in range(len(self.log_file)):
            for j in range(5):
                table_widget.setItem(i, j, QTableWidgetItem(self.log_file[i][j]))

            table_widget.setItem(i, 5, QTableWidgetItem(""))
            if self.log_file[i][5]:
                table_widget.item(i, 5).setCheckState(QtCore.Qt.Checked)
            else:
                table_widget.item(i, 5).setCheckState(QtCore.Qt.Unchecked)

    # Takes a list of log entries and a table widget, populates the table widget with the log entries in the list
    def populate_logentry_table(self, table_widget, logentries):
        table_widget.setRowCount(len(logentries))

        for i in range(len(logentries)):
            table_widget.setRowHeight(i, 60)
            table_widget.setItem(i, 1, QTableWidgetItem(str(logentries[i].serial)))
            table_widget.setItem(i, 2, QTableWidgetItem(logentries[i].timestamp))
            table_widget.setItem(i, 3, QTableWidgetItem(logentries[i].content))

            table_widget.setItem(i, 0, QTableWidgetItem(""))
            if logentries[i].checked:
                table_widget.item(i, 0).setCheckState(QtCore.Qt.Checked)
            else:
                table_widget.item(i, 0).setCheckState(QtCore.Qt.Unchecked)

            table_widget.setItem(i, 4, QTableWidgetItem(logentries[i].get_vector_list_str()))

    def populate_vector_table(self, table_widget, vector_num):
        if len(self.vectors) == 0 or vector_num < 0 or vector_num >= len(self.vectors):
            return

        table_widget.setRowCount(len(self.vectors[vector_num].get_nodes()))
        for i in range(len(self.vectors[vector_num].get_nodes())):
            table_widget.setItem(i, 0, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].get_id()))
            table_widget.setItem(i, 1, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].name))
            table_widget.setItem(i, 2, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].get_timestamp()))
            table_widget.setItem(i, 3, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].description))
            table_widget.setItem(i, 4, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].get_reference()))
            table_widget.setItem(i, 5, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].log_creator))
            table_widget.setItem(i, 6, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].event_type))
            table_widget.setItem(i, 7, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].icon_type))
            table_widget.setItem(i, 8, QTableWidgetItem(self.vectors[vector_num].get_nodes()[i].source))

            table_widget.setItem(i, 9, QTableWidgetItem(""))
            if self.vectors[vector_num].get_nodes()[i].is_visible():
                table_widget.item(i, 9).setCheckState(QtCore.Qt.Checked)
            else:
                table_widget.item(i, 9).setCheckState(QtCore.Qt.Unchecked)

    def populate_vectorconfiguration_table(self, table_widget):
        table_widget.setRowCount(len(self.vectors))

        for i in range(len(self.vectors)):
            table_widget.setItem(i, 0, QTableWidgetItem(""))
            if self.vectors[i].is_checked_config():
                table_widget.item(i, 0).setCheckState(QtCore.Qt.Checked)
            else:
                table_widget.item(i, 0).setCheckState(QtCore.Qt.Unchecked)

            table_widget.setItem(i, 1, QTableWidgetItem(self.vectors[i].name))
            table_widget.setItem(i, 2, QTableWidgetItem(self.vectors[i].description))

    def populate_relationship_table(self, table_widget, vector_num):
        if len(self.vectors) == 0 or vector_num < 0 or vector_num >= len(self.vectors):
            return

        table_widget.setRowCount(len(self.vectors[vector_num].get_relationships()))
        for i in range(len(self.vectors[vector_num].get_relationships())):
            table_widget.setItem(i, 0, QTableWidgetItem(self.vectors[vector_num].get_relationships()[i].get_id_str()))
            table_widget.setItem(i, 1, QTableWidgetItem(self.vectors[vector_num].get_relationships()[i].get_name()))
            table_widget.setItem(i, 2, QTableWidgetItem(self.vectors[vector_num].get_relationships()[i].get_parent_id()))
            table_widget.setItem(i, 3, QTableWidgetItem(self.vectors[vector_num].get_relationships()[i].get_child_id()))

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

    def add_vector(self):
        self.vectors.append(Vector(name="Vector " + str(len(self.vectors)+1)))
        print("added vector")

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

    def edit_node_table(self, row, column, value, vector_num):
        if column == 9:
            self.vectors[vector_num].nodes[row].visibility = value
        elif column == 1:
            self.vectors[vector_num].nodes[row].name = value
        elif column == 3:
            self.vectors[vector_num].nodes[row].description = value
        return

    def edit_vector_table(self, row, column, value):
        if column == 0:
            self.vectors[row].checked_configuration_table = value
        elif column == 1:
            self.vectors[row].name = value
        elif column == 3:
            self.vectors[row].description = value
        return

    def export_table_to_csv(self, list2d, filename="output.csv"):
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(list2d)

    def populate_enforcement_action_report_table(self, log_file):
        self.enforcement_action_report_table.setRowCount(len(log_file.errors))
        for i in range(len(log_file.errors)):
            self.enforcement_action_report_table.setItem(i, 0, QTableWidgetItem(str(log_file.errors[i][0])))
            self.enforcement_action_report_table.setItem(i, 1, QTableWidgetItem(log_file.errors[i][1]))

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

    def add_log_entries_to_vectors(self, selected_log_entries, log_entries, selected_vectors):
        for i in selected_log_entries:
            for j in selected_vectors:
                self.vectors[j].add_node(Node.node_from_log_entry(log_entries[i]))