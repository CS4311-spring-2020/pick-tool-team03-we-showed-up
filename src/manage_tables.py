from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import math
from demo_data import DemoData
from random import randint
import csv


class manage_tables:
    def __init__(self):
        self.enforcement_action_report_table = None
        pass


    fake_data = DemoData()

    log_file = [["observer_log_1.txt", "c:\logs\observer\\feblogs", "100%", "100%", "100%", True],
                ["observer_log_2.txt", "c:\logs\observer\marchlogs", "100%", "100%", "100%", False],
                ["observer_log_3.txt", "c:\logs\\redteam\\feblogs", "100%", "100%", "100%", False]]

    enforcement_action_1 = [["00006", "Timestamp out of range"],
                            ["1012", "Empty line"],
                            ["1210", "Unreadable line format"]]

    enforment_action_reports = [enforcement_action_1]

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
        if vector_num < 0:
            return
        table_widget.setRowCount(len(self.fake_data.vector_list[vector_num].nodes))

        for i in range(len(self.fake_data.vector_list[vector_num].nodes)):
            for j in range(9):
                table_widget.setItem(i, j, QTableWidgetItem(self.fake_data.vector_list[vector_num].nodes[i][j]))

            table_widget.setItem(i, 9, QTableWidgetItem(""))
            if self.fake_data.vector_list[vector_num].nodes[i][9]:
                table_widget.item(i, 9).setCheckState(QtCore.Qt.Checked)
            else:
                table_widget.item(i, 9).setCheckState(QtCore.Qt.Unchecked)

    def populate_vectorconfiguration_table(self, table_widget):
        table_widget.setRowCount(len(self.fake_data.vector_list))

        for i in range(len(self.fake_data.vector_list)):
            table_widget.setItem(i, 0, QTableWidgetItem(""))
            if self.fake_data.vector_list[i].vector_checked:
                table_widget.item(i, 0).setCheckState(QtCore.Qt.Checked)
            else:
                table_widget.item(i, 0).setCheckState(QtCore.Qt.Unchecked)

            table_widget.setItem(i, 1, QTableWidgetItem(self.fake_data.vector_list[i].vector_name))
            table_widget.setItem(i, 2, QTableWidgetItem(self.fake_data.vector_list[i].vector_description))

    def populate_enforcementactionreports_table(self, table_widget, vector_num):
        table_widget.setRowCount(len(self.enforment_action_reports[vector_num]))

        for i in range(len(self.enforment_action_reports[vector_num])):
            for j in range(2):
                table_widget.setItem(i, j, QTableWidgetItem(self.enforment_action_reports[vector_num][i][j]))

    def populate_relationship_table(self, table_widget, vector_num):
        table_widget.setRowCount(len(self.fake_data.vector_list[vector_num].relationships))

        for i in range(len(self.fake_data.vector_list[vector_num].relationships)):
            for j in range(4):
                table_widget.setItem(i, j, QTableWidgetItem(self.fake_data.vector_list[vector_num].relationships[i][j]))

    def populate_vector_dropdowns(self, combo_box):
        combo_box.clear()

        for i in range(len(self.fake_data.vector_list)):
            combo_box.addItem(self.fake_data.vector_list[i].vector_name)

    def add_vector(self):
        self.fake_data.add_vector()
        print("added vector")
        for i in range(len(self.fake_data.vector_list)):
            print("Vector #", i, " ", self.fake_data.vector_list[i].vector_name)

    def create_node(self, vector_num):
        newNode = [str(randint(0, 9999)), '', '', '', '', '', '', '', '', True]
        self.fake_data.vector_list[vector_num].nodes.insert(0, newNode)

    def create_relationship(self, vector_num):
        new_relationship = [str(randint(0, 999)), '', '', '']
        self.fake_data.vector_list[vector_num].relationships.insert(0, new_relationship)

    def edit_node_table(self, row, column, value, vector_num):
        self.fake_data.vector_list[vector_num].nodes[row][column] = value

    def export_table_to_csv(self, list2d, filename="output.csv"):
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(list2d)


    def update_enforcement_action_report_table(self, logFiles):
        for f in logFiles:
            if f.is_invalid():
                print("")