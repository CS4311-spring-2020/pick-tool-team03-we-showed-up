import math
from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import *
from UI.mainwindow import Ui_PICK
from UI.IP_Error_ConnectionLimitReached import Ui_Dialog as UIConnectionLimit
from UI.IP_Error_duplicateLeadIP import Ui_Dialog as UIDuplicateLeadIP
from UI.IP_Error_LeadIPBoxSelected import Ui_Dialog as UILeadIPSelected
from UI.IP_Error_LeadIPNotProvided import Ui_Dialog as UILeadIPNotProvided
from UI.icon_Configuration_Dialog import Ui_Dialog as UIIconConfigDialog
from UI.vector_DB_Lead import Ui_Dialog as UIVectorDBLead
from UI.vector_DB_Analyst import Ui_Dialog as UIVectorDBAnalyst
from UI.logentrydescription import Ui_Dialog as LogEntryDescription
from UI.EventConfigurationNew import Ui_Dialog as UiEventConfigNew
from UI.EventConfigurationOpen import Ui_Dialog as UiEventConfigOpen
from UI.EventConfigurationEdit import Ui_Dialog as UiEventConfigEdit
from UI.SPLUNK_Login_Dialog import Ui_Dialog as SPLUNKLoginDialog
from UI.Create_Relationship_Dialog import Ui_Dialog as RelationshipDialog
from Graph import GraphInterface
import sys


class UIMain(Ui_PICK):
    """This class serves as the main user interface for the PICK Tool, it inherits from the QT mainwindow and serves
    adds the functionality for the button presses, menu changes and other UI-related operations.
        """
    user_change = True

    def __init__(self, table_manager=None, controller=None, network=None,
                 undo_manager=None, event_session=None, db=None):
        self.table_manager = table_manager
        self.network = network
        self.undo_manager = undo_manager
        self.controller = controller
        self.event_session = event_session
        self.db = db

    # Sets the table manager for this UI to manage all QTableWidget items
    def set_table_manager(self, table_manager):
        self.table_manager = table_manager

    # Main setup of the UI,
    def setupUi(self, pick):
        super().setupUi(pick)

        self.vc_undo_button.clicked.connect(self.undo_manager.undo)

        # Sets the graph widget
        self.vc_graph_widget = GraphInterface(self.horizontalLayout_13)
        self.controller.graph = self.vc_graph_widget

        # Set the tables to be managed
        self.table_manager.set_enforcement_action_report_table(self.tableWidget_2)
        self.table_manager.set_log_file_table(self.tableWidget)
        self.table_manager.set_log_entry_table(self.lec_logentry_table)
        self.table_manager.set_node_table(self.vc_node_table)
        self.table_manager.set_relationship_table(self.vc_relationship_table)
        self.table_manager.set_vector_config_table(self.vc_table)
        self.table_manager.vector_drop_down = self.vc_vector_drop_down
        self.table_manager.add_to_vector_table = self.lec_add_to_vector_table

        # Initial setup of table data
        self.controller.update_log_entry_table()
        self.controller.update_vector_tables()
        self.controller.update_node_and_relationship_tables()
        self.controller.update_vector_dropdwon()

        # Sets actions from the File Menu
        self.actionNew.triggered.connect(self.open_new_event_config)
        self.actionOpen.triggered.connect(self.open_events_config)
        self.actionEdit.triggered.connect(self.edit_event_config)

        # Sets up right-click menu for the Log Entry table
        self.lec_logentry_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.lec_logentry_table.customContextMenuRequested.connect(self.rightClickLogEntry)

        # Setup of add/delete buttons
        self.vc_vector_drop_down.currentIndexChanged.connect(self.vector_dropdown_select)
        self.button_add_vector.clicked.connect(self.add_vector)
        self.button_delete_vector.clicked.connect(self.delete_vector)
        self.vc_add_relationship_button.clicked.connect(self.create_relationship_button_clicked)
        self.vc_add_button.clicked.connect(self.controller.create_node)
        self.lec_add_to_vector_button.clicked.connect(self.add_log_entry_to_vector)

        # Setup of network-related buttons
        self.checkBox_lead.stateChanged.connect(self.connect_lead_clicked)
        self.button_connect_to_ip.clicked.connect(self.connect_button_clicked)
        self.nc_iconchange_button.clicked.connect(self.icon_edit_button_clicked)
        self.vc_push_button.clicked.connect(self.vector_db_button_clicked)

        # setup of validate button in the enforcement action report table
        self.pushButton_3.clicked.connect(self.controller.validate_anyway_clicked)

        # setup of filter button in Log Entry table
        self.fc_applyfilter_button.clicked.connect(self.filter_log_entries)

        # Sets up methods for export table functions
        self.ec_export_button.clicked.connect(lambda: self.export_table_clicked("log entry"))
        self.nc_export_button.clicked.connect(lambda: self.export_table_clicked("node"))
        self.vc_export_pushButton.clicked.connect(lambda: self.export_table_clicked("vector"))

        # Connects the item change signals to edition functions
        self.vc_node_table.itemChanged.connect(self.edit_table_node)
        self.tableWidget.itemChanged.connect(self.edit_table_log_files)
        self.vc_table.itemChanged.connect(self.edit_table_vector_configuration)
        self.lec_logentry_table.itemChanged.connect(self.edit_table_log_entry)

    # Notifies the SPLUNK Facade to refresh the log entries given the user input
    def filter_log_entries(self):
        self.user_change = False
        if self.fc_start_time.dateTime() > self.fc_end_time.dateTime():
            print("invalid date range in filtering")
            return
        self.controller.update_splunk_filter(self.fc_keyword_line_input.text())
        self.user_change = True

    # Event Configuration Methods
    def open_new_event_config(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = UiEventConfigNew()
        ec_ui.setupUi(ec_dialog)
        ec_ui.button_save_event.clicked.connect(lambda: self.call_create_index(ec_ui))

        ec_ui.textbox_root_directory.setPlainText(self.event_session.get_root_path())
        ec_ui.textbox_white_team_folder.setPlainText(self.event_session.get_white_team_path())
        ec_ui.textbox_red_team_folder.setPlainText(self.event_session.get_red_team_path())
        ec_ui.textbox_blue_team_folder.setPlainText(self.event_session.get_blue_team_path())

        # save directories of teams
        ec_ui.button_start_ingestion.clicked.connect(self.controller.start_ingestion)
        ec_ui.root_directory_pushButton.clicked.connect(
            lambda: self.open_ingestion_directory_selector(ec_ui.textbox_root_directory, team="root"))
        ec_ui.red_team_directory_pushButton.clicked.connect(
            lambda: self.open_ingestion_directory_selector(ec_ui.textbox_red_team_folder, team="red"))
        ec_ui.blue_team_directory_pushButton.clicked.connect(
            lambda: self.open_ingestion_directory_selector(ec_ui.textbox_blue_team_folder, team="blue"))
        ec_ui.white_team_directory_pushButton.clicked.connect(
            lambda: self.open_ingestion_directory_selector(ec_ui.textbox_white_team_folder, team="white"))
        ec_dialog.exec_()

    # Sends user changes to edit the event configuration
    # TODO: make it work with database
    def edit_event_config(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = UiEventConfigEdit()
        ec_ui.setupUi(ec_dialog)

        ec_ui.textbox_root_directory_edit.setPlainText(self.event_session.get_root_path())
        ec_ui.textbox_white_team_folder.setPlainText(self.event_session.get_white_team_path())
        ec_ui.textbox_red_team_folder_edit.setPlainText(self.event_session.get_red_team_path())
        ec_ui.textbox_blue_team_folder_edit.setPlainText(self.event_session.get_blue_team_path())

        events = self.db.get_event_names()
        for event in events:
            ec_ui.comboBox.addItem(event)
        # ec_ui.button_save_event.clicked.connect
        ec_dialog.exec_()

    # Helper method to be used to notify the SPLUNK tool to create an index
    def call_create_index(self, ec_ui):
        if ec_ui.dateTimeEdit.dateTime() >= ec_ui.date_event_end.dateTime():
            ec_ui.event_creation_status_label.setText("Sorry, time range is invalid.")
            return
        event_name = ec_ui.textbox_event_name.toPlainText()
        event_description = ec_ui.textbox_event_description.toPlainText()
        start_time = ec_ui.dateTimeEdit.dateTime().toPyDateTime()
        end_time = ec_ui.date_event_end.dateTime().toPyDateTime()

        flag = self.controller.create_event(event_name, event_description, start_time, end_time)

        if flag == 1:
            ec_ui.event_creation_status_label.setText("Sorry, event name is taken.")
        elif flag == 2:
            ec_ui.event_creation_status_label.setText("Sorry, connect to SPLUNK first")
        elif flag == 3:
            ec_ui.event_creation_status_label.setText("Sorry, valid names should be lowercase and contain no spaces")
        else:
            text = "Event " + event_name + " added."
            ec_ui.event_creation_status_label.setText(text)

    # Open Event
    def open_events_config(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = UiEventConfigOpen()
        ec_ui.setupUi(ec_dialog)
        # call list of indexes and display event
        events = self.db.get_event_names()
        for event in events:
            ec_ui.comboBox.addItem(event)
        ec_ui.ok_button.clicked.connect(lambda: self.update_open_event_config(ec_ui, events))
        ec_dialog.exec_()

    def update_open_event_config(self, ec_ui, event_list):
        # text = ec_ui.comboBox.currentData()
        # print(text)
        # ec_ui.label_3.setText(text)
        e_map = self.db.get_event_map()
        selected_event = event_list[ec_ui.comboBox.currentIndex()]
        print(e_map[selected_event])
        self.controller.update_event_data(e_map[selected_event])
        self.controller.update_node_and_relationship_tables()
        self.controller.update_vector_tables()
        self.controller.update_vector_dropdwon()

    # Vector
    def add_vector(self):
        self.user_change = False
        self.controller.add_vector()
        self.user_change = True

    def delete_vector(self):
        self.user_change = False
        if self.vector_deletion_confirmation() == 1024:
            print("Deleting vector(s)")
            self.controller.delete_vector()
        self.user_change = True

    def vector_deletion_confirmation(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Are you sure you want to delete the vector(s)?")
        msg.setWindowTitle("Vector Deletion")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        return retval

    def rightClickLogEntry(self, point):
        index = self.lec_logentry_table.indexAt(point)

        if not index.isValid():
            return

        menu = QtWidgets.QMenu()
        menu.addAction("Show full description", self.log_entry_description_button_clicked)
        menu.exec_(self.lec_logentry_table.mapToGlobal(point))

    def edit_table_log_files(self, item):
        if not self.user_change:
            return
        print("changing log table")
        if item.column() == 5:
            self.user_change = False
            self.event_session.log_files[item.row()].marked = not (item.checkState() == 0)

            if not (item.checkState() == 0):
                self.label_12.setText(self.event_session.get_log_files()[item.row()].get_name())
                self.table_manager.populate_enforcement_action_report_table(self.event_session.get_log_files()[item.row()])

            numlist = list(range(len(self.event_session.get_log_files())))
            numlist.remove(item.row())

            for i in numlist:
                self.event_session.get_log_files()[i].marked = False
                self.tableWidget.setItem(i, 5, QTableWidgetItem(""))
                self.tableWidget.item(i, 5).setCheckState(QtCore.Qt.Unchecked)

            self.user_change = True

    def edit_table_log_entry(self, item):
        if not self.user_change:
            return
        self.user_change = False
        try:
            for i in range(self.lec_logentry_table.rowCount()):
                if self.lec_logentry_table.item(i, 0).isSelected():
                    self.lec_logentry_table.item(i, 0).setCheckState(item.checkState())
        except AttributeError:
            print("edit log entry table triggered pre")

        self.user_change = True

    def edit_table_node(self, item):
        if not self.user_change:
            return
        self.user_change = False
        if item.column() == 0:
            self.controller.update_node_table()
        elif item.column() == 9:
            self.controller.edit_node_table(item.row(), item.column(), (not item.checkState() == 0))
        else:
            self.vc_graph_widget.save_node_positions(self.event_session.get_selected_vector())
            self.controller.edit_node_table(item.row(), item.column(), item.text())
        try:
            if self.vc_vector_drop_down.currentIndex() >= 0:
                self.vc_graph_widget.save_node_positions(self.event_session.get_selected_vector())
                self.vc_graph_widget.set_vector(self.event_session.get_selected_vector())
        except IndexError:
            print("Wrong index of vector")
        self.user_change = True

    def edit_table_vector_configuration(self, item):
        if not self.user_change:
            return
        self.user_change = False
        if item.column() == 0:
            self.controller.edit_vector_configuration_table(item.row(), item.column(),
                                                            (not item.checkState() == 0))
        else:
            self.controller.edit_vector_configuration_table(item.row(), item.column(), item.text())
        self.controller.update_vector_tables()
        self.controller.update_vector_dropdwon()
        self.user_change = True

    def resize_ui_components(self, PICK):
        self.set_column_widths_log_entry_tab()
        self.set_column_widths_event_tab()
        self.set_column_widths_vector_view_tab()

    def add_log_entry_to_vector(self):
        selected_entries = []
        for i in range(self.lec_logentry_table.rowCount()):
            if not self.lec_logentry_table.item(i, 0).checkState() == 0:
                print("Checked item at position: ", i)
                selected_entries.append(i)

        selected_vectors = []
        for i in range(self.lec_add_to_vector_table.rowCount()):
            if not self.lec_add_to_vector_table.item(i, 0).checkState() == 0:
                print("Checked item at position: ", i)
                selected_vectors.append(i)

        self.controller.add_log_entry_to_vector(selected_entries, selected_vectors)
        self.vector_dropdown_select()
        return

    # Calls the connection methods once the buttons is clicked
    def connect_button_clicked(self):
        lead_ip = "64.233. 160.0"  # currently Google's IP
        no_connections = 10  # temporary placeholder for number of connections

        bt_dialog = QtWidgets.QDialog()

        if self.textbox_ip.toPlainText() == lead_ip:
            print("open same ip error prompt")
            bt_ui = UIDuplicateLeadIP()
            bt_ui.setupUi(bt_dialog)
            bt_ui.pushButton.clicked.connect(bt_dialog.close)
            bt_dialog.exec_()

        elif self.textbox_ip.toPlainText() == "":
            print("no lead ip error prompt")
            bt_ui = UILeadIPNotProvided()
            bt_ui.setupUi(bt_dialog)
            bt_ui.pushButton.clicked.connect(bt_dialog.close)
            bt_dialog.exec_()

        elif self.checkBox_lead.isChecked():
            print("lead checked error prompt")
            bt_ui = UILeadIPSelected()
            bt_ui.setupUi(bt_dialog)
            bt_ui.pushButton.clicked.connect(bt_dialog.close)
            bt_dialog.exec_()

        elif no_connections > 20:
            print("max connections error prompt")
            bt_ui = UIConnectionLimit()
            bt_ui.setupUi(bt_dialog)
            bt_ui.pushButton.clicked.connect(bt_dialog.close)
            bt_dialog.exec_()

        else:
            print("successful connection should take place.")

    # Opens the icon edit window
    def icon_edit_button_clicked(self):
        ic_dialog = QtWidgets.QDialog()
        ic_ui = UIIconConfigDialog()
        ic_ui.setupUi(ic_dialog)
        ic_dialog.exec_()

    # Opens the log entry description window
    def log_entry_description_button_clicked(self):
        ic_dialog = QtWidgets.QDialog()
        ic_ui = LogEntryDescription()
        ic_ui.setupUi(ic_dialog)
        ic_dialog.exec_()

    # Opens the VCS window
    def vector_db_button_clicked(self):
        vdb_dialog = QtWidgets.QDialog()
        if self.checkBox_lead.isChecked():
            vdb_ui = UIVectorDBLead()
            vdb_ui.setupUi(vdb_dialog)
            vdb_ui.vdbcl_button_commit.clicked.connect(self.controller.update_event_db)
        else:
            vdb_ui = UIVectorDBAnalyst()
            vdb_ui.setupUi(vdb_dialog)
            # vdb_ui.vdbc_button_push.clicked.connect(self.database.save_vector_to_database())
            # vdb_ui.vdbc_button_pull.clicked.connect(self.database.update_vector)

        vdb_dialog.exec_()

    # Sends the vector selection from the user
    def vector_dropdown_select(self):
        if not self.user_change:
            return
        self.user_change = False
        sel_vec = self.vc_vector_drop_down.currentIndex()
        print("Changed vector to: ", sel_vec)
        try:
            if sel_vec >= 0:
                self.controller.set_display_vector(sel_vec)
                self.controller.update_node_and_relationship_tables()
        except IndexError:
            print("No vector to be selected")
        self.user_change = True

    # Method called when a the export button of a table is clicked
    def export_table_clicked(self, key):
        option = QFileDialog.Options()
        if key == "node":
            filename = QFileDialog.getSaveFileName(None, 'Export Graph', '', 'PNG (*.png)', options=option)
        else:
            filename = QFileDialog.getSaveFileName(None, 'Export Graph', '', 'CSV (*.csv)', options=option)

        if filename is not None:
            filename = str(filename[0])
            if filename == '':  # if no filename just omit
                return
            if self.nc_export_dropdown.currentIndex() == 1 and key == "node":  # if png option was selected
                print("Export Graph as image")
                self.vc_graph_widget.export(filename)
                return
            print("Exporting csv to: ", filename)
            switcher = {
                "log entry": lambda: self.controller.export_log_entry_table(filename=filename),
                "node": lambda: self.controller.export_node_table(filename=filename),
                "vector": lambda: self.controller.export_vector_configuration_table(filename=filename)}
            switcher[key]()

    # Calls the creation of a node when the button is clicked
    def create_node_button_clicked(self):
        self.controller.create_node()
        self.controller.update_node_table()
        sel_vec = self.vc_vector_drop_down.currentIndex()
        try:
            self.vc_graph_widget.set_vector(self.event_session.get_selected_vector())
        except IndexError:
            print("no vector available")

    # Opens a dialog when the create relationship button is clicked
    def create_relationship_button_clicked(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = RelationshipDialog()
        ec_ui.setupUi(ec_dialog)
        self.controller.update_node_dropdowns(ec_ui.child_id_combobox)
        self.controller.update_node_dropdowns(ec_ui.parent_id_combobox)

        ec_ui.create_button.clicked.connect(lambda: self.controller.create_relationship(
            ec_ui.parent_id_combobox.currentIndex(),
            ec_ui.child_id_combobox.currentIndex(),
            ec_ui.name_line_edit.text()
        ))
        ec_dialog.exec_()

        try:
            self.vc_graph_widget.set_vector(self.event_session.get_selected_vector())
        except IndexError:
            print("no vector available")

    # Opens a dialog for the user to select the folder to be ingested
    def open_ingestion_directory_selector(self, textbox_widget=None, team="root"):
        directory = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        if textbox_widget is None:
            print(directory)
        else:
            self.controller.update_folder_path(team, directory)
            textbox_widget.setPlainText(str(directory))

    # When the user marks themselves as a lead it calls the relevant operations and sets the state as lead
    def connect_lead_clicked(self):
        if self.checkBox_lead.isChecked():
            ec_dialog = QtWidgets.QDialog()
            ec_ui = SPLUNKLoginDialog()
            ec_ui.setupUi(ec_dialog)
            ec_ui.push_button_connect.clicked.connect(lambda: self.connect_lead(ec_ui))
            ec_ui.push_button_cancel.clicked.connect(lambda: self.checkBox_lead.setCheckState(QtCore.Qt.Unchecked))
            ec_dialog.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Incorrect Splunk login credentials.")
            msg.setWindowTitle("Unsuccessful Splunk Connection")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            print("lead unchecked, must disconnect")

    # Helper method that asks the SPLUNK interface to connect given the user's input
    def connect_lead(self, ec_ui):
        print("Connecting client to Splunk ...")
        if self.controller.connect_to_splunk(ec_ui.line_edit_username.text(), ec_ui.line_edit_password.text()):
            print("Splunk connected successfully")
        else:
            print("Splunk connection failed")
            self.checkBox_lead.setCheckState(QtCore.Qt.Unchecked)

    def set_column_widths_log_entry_tab(self):
        # Sets columns width for the log entry table
        # logentry_table_width = self.lec_logentry_table.width()
        logentry_table_width = 1036
        logentry_table_width -= 5
        column_width = math.floor(logentry_table_width * .06)
        self.lec_logentry_table.setColumnWidth(0, column_width)
        column_width = math.floor(logentry_table_width * .10)
        self.lec_logentry_table.setColumnWidth(1, column_width)
        column_width = math.floor(logentry_table_width * .24)
        self.lec_logentry_table.setColumnWidth(2, column_width)
        column_width = math.floor(logentry_table_width * .53)
        self.lec_logentry_table.setColumnWidth(3, column_width)
        column_width = math.floor(logentry_table_width * .07)
        self.lec_logentry_table.setColumnWidth(4, column_width)

    def set_column_widths_event_tab(self):
        # for Vector Configuration table
        # vc_table_width = self.vc_table.width()
        vc_table_width = 440
        vc_table_width -= 5
        column_width = math.floor(vc_table_width * .07)
        self.vc_table.setColumnWidth(0, column_width)
        column_width = math.floor(vc_table_width * .30)
        self.vc_table.setColumnWidth(1, column_width)
        column_width = math.floor(vc_table_width * .63)
        self.vc_table.setColumnWidth(2, column_width)

        # for Enforcement Action Report
        # ear_table_width = self.tableWidget_2.width()
        ear_table_width = 560
        ear_table_width -= 5
        column_width = math.floor(ear_table_width * .25)
        self.tableWidget_2.setColumnWidth(0, column_width)
        column_width = math.floor(ear_table_width * .75)
        self.tableWidget_2.setColumnWidth(1, column_width)

        # for Log File Configuration
        # lfc_table_width = self.tableWidget.width()
        lfc_table_width = 540
        lfc_table_width -= 5
        column_width = math.floor(lfc_table_width * .15)
        self.tableWidget.setColumnWidth(0, column_width)
        column_width = math.floor(lfc_table_width * .18)
        self.tableWidget.setColumnWidth(1, column_width)
        column_width = math.floor(lfc_table_width * .18)
        self.tableWidget.setColumnWidth(2, column_width)
        column_width = math.floor(lfc_table_width * .18)
        self.tableWidget.setColumnWidth(3, column_width)
        column_width = math.floor(lfc_table_width * .18)
        self.tableWidget.setColumnWidth(4, column_width)
        column_width = math.floor(lfc_table_width * .13)
        self.tableWidget.setColumnWidth(5, column_width)

    def set_column_widths_vector_view_tab(self):
        # for Vector Node table
        vnode_table_width = 850
        vnode_table_width -= 5
        column_width = math.floor(vnode_table_width * .1)
        for i in range(0, 10):
            self.vc_node_table.setColumnWidth(i, column_width)

        # for Relationship Table
        vrelationship_table_width = 600
        vrelationship_table_width -= 5
        column_width = math.floor(vrelationship_table_width * .25)
        for i in range(0, 4):
            self.vc_relationship_table.setColumnWidth(i, column_width)


if __name__ == "__main__":
    app = QApplication([])
    PICK = QtWidgets.QMainWindow()
    path = QtGui.QPainterPath()
    scene = QtWidgets.QGraphicsScene()
    ui = UIMain()
    ui.setupUi(PICK)
    PICK.show()
    ui.resize_ui_components(PICK)
    sys.exit(app.exec_())
