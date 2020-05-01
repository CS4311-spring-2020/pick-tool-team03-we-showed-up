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
from graph import graph
from Connections.Database import Database
import sys
import threading
import time


class functionality(Ui_PICK):

    user_change = True

    def __init__(self, table_manager=None, splunk=None, event_config=None, ingest_funct=None, network=None):
        self.table_manager = table_manager
        self.splunk = splunk
        self.event_config = event_config
        self.ingest_funct = ingest_funct
        self.network = network
        self.database = Database()
        pass

    def set_splunk(self, splunk):
        self.splunk = splunk

    def set_table_manager(self, table_manager):
        self.table_manager = table_manager

    def set_event_config(self, event_config):
        self.event_config = event_config

    def set_ingestion_funct(self, ingestion_func):
        self.ingest_funct = ingestion_func

    def setupUi(self, PICK):
        super().setupUi(PICK)

        self.vc_graph_widget = graph(self.horizontalLayout_13)

        # Set the tables to be managed
        self.table_manager.set_enforcement_action_report_table(self.tableWidget_2)
        self.table_manager.set_log_file_table(self.tableWidget)
        self.table_manager.set_log_entry_table(self.lec_logentry_table)
        self.table_manager.set_node_table(self.vc_node_table)
        self.table_manager.set_relationship_table(self.vc_relationship_table)
        self.table_manager.set_vector_config_table(self.vc_table)

        # self.vc_add_button.clicked.connect(self.add_node)
        self.table_manager.populate_logentry_table(self.splunk.logentries)
        self.table_manager.populate_relationship_table(0)
        self.table_manager.populate_node_table(0)
        self.table_manager.populate_vector_configuration_table()
        self.table_manager.populate_vector_dropdowns(self.vc_vector_drop_down)
        self.vc_vector_drop_down.currentIndexChanged.connect(self.vector_dropdown_select)
        self.button_add_vector.clicked.connect(self.add_vector)
        self.vc_add_relationship_button.clicked.connect(self.createrelationship_button_triggered)

        self.lec_logentry_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.lec_logentry_table.customContextMenuRequested.connect(self.rightClickLogEntry)

        self.ec_export_button.clicked.connect(lambda: self.export_table_clicked("log entry"))
        self.nc_export_button.clicked.connect(lambda: self.export_table_clicked("node"))
        self.vc_export_pushButton.clicked.connect(lambda: self.export_table_clicked("vector"))

        self.vc_node_table.itemChanged.connect(self.edit_table_node)
        self.tableWidget.itemChanged.connect(self.log_table_clicked)
        self.vc_table.itemChanged.connect(self.edit_table_vector_configuration)
        self.lec_logentry_table.itemChanged.connect(self.edit_table_log_entry)

        # SPLUNK
        self.actionNew.triggered.connect(self.open_new_event_config)
        self.actionOpen.triggered.connect(self.open_events_config)
        self.actionEdit.triggered.connect(self.edit_event_config)

        self.pushButton_3.clicked.connect(lambda: self.ingest_funct.validate_file_anyway(self.event_config.name, self.splunk))
        self.checkBox_lead.stateChanged.connect(self.connect_lead_triggered)

        self.fc_applyfilter_button.clicked.connect(self.filter_log_entries)

    def filter_log_entries(self):
        self.user_change = False
        if self.fc_start_time.dateTime() > self.fc_end_time.dateTime():
            print("invalid date range in filtering")
            return

        # FORMAT IS 10/5/2016:20:00:00
        print("filtering to keyword: ", self.fc_keyword_line_input.text())
        self.splunk.set_keyword(self.fc_keyword_line_input.text())
        #print("Earliest time is: ", self.fc_start_time.dateTime().toPyDateTime().timestamp())
        #self.splunk.set_earliest_time(self.fc_start_time.dateTime().toString("dd/MM/yyyy:hh:mm:ss"))
        #print("Latest time is: ", self.fc_end_time.dateTime().toString("dd/MM/yyyy:hh:mm:ss"))
        # self.splunk.set_latest_time(self.fc_end_time.dateTime().toString("dd/MM/yyyy:hh:mm:ss"))

        self.splunk.get_log_count(bypass_check=True)
        self.table_manager.populate_logentry_table(self.splunk.logentries)
        self.user_change = True

    #SPLUNK - New Event
    def open_new_event_config(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = UiEventConfigNew()
        ec_ui.setupUi(ec_dialog)
        ec_ui.button_save_event.clicked.connect(lambda: self.call_create_index(ec_ui))

        ec_ui.textbox_root_directory.setPlainText(self.event_config.rootpath)
        ec_ui.textbox_white_team_folder.setPlainText(self.event_config.whitefolder)
        ec_ui.textbox_red_team_folder.setPlainText(self.event_config.redfolder)
        ec_ui.textbox_blue_team_folder.setPlainText(self.event_config.bluefolder)

        #save directories of teams
        ec_ui.button_start_ingestion.clicked.connect(self.start_ingestion)
        ec_ui.root_directory_pushButton.clicked.connect(lambda: self.open_ingestion_directory_selector(ec_ui.textbox_root_directory, team=0))
        ec_ui.red_team_directory_pushButton.clicked.connect(lambda: self.open_ingestion_directory_selector(ec_ui.textbox_red_team_folder, team=1))
        ec_ui.blue_team_directory_pushButton.clicked.connect(lambda: self.open_ingestion_directory_selector(ec_ui.textbox_blue_team_folder, team=2))
        ec_ui.white_team_directory_pushButton.clicked.connect(lambda: self.open_ingestion_directory_selector(ec_ui.textbox_white_team_folder, team=3))
        ec_dialog.exec_()

    #SPLUNK - Edit Event
    def edit_event_config(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = UiEventConfigEdit()
        ec_ui.setupUi(ec_dialog)

        ec_ui.textbox_root_directory_edit.setPlainText(self.event_config.rootpath)
        ec_ui.textbox_white_team_folder.setPlainText(self.event_config.whitefolder)
        ec_ui.textbox_red_team_folder_edit.setPlainText(self.event_config.redfolder)
        ec_ui.textbox_blue_team_folder_edit.setPlainText(self.event_config.bluefolder)

        events = self.splunk.getIndexList()
        for event in events:
            ec_ui.comboBox.addItem(event)
        ec_ui.button_save_event.clicked.connect
        ec_dialog.exec_()

    def call_create_index(self, ec_ui):
        if (ec_ui.dateTimeEdit.dateTime() >= ec_ui.date_event_end.dateTime()):
            ec_ui.event_creation_status_label.setText("Sorry, time range is invalid.")
            return
        event_name = ec_ui.textbox_event_name.toPlainText()
        event_description = ec_ui.textbox_event_description.toPlainText()
        flag = self.splunk.createEvent(event_name, event_description)
        if flag == 1:
            ec_ui.event_creation_status_label.setText("Sorry, event name is taken.")
        else:
            text = "Event " + event_name + " added."
            self.event_config.name = event_name
            self.event_config.description = event_description
            self.event_config.starttime = ec_ui.dateTimeEdit.dateTime().toPyDateTime()
            self.event_config.endtime = ec_ui.date_event_end.dateTime().toPyDateTime()
            ec_ui.event_creation_status_label.setText(text)

    #SPLUNK - Open Event
    def open_events_config(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = UiEventConfigOpen()
        ec_ui.setupUi(ec_dialog)
        #call list of indexes and display event
        events = self.splunk.getIndexList()
        for event in events:
            ec_ui.comboBox.addItem(event)
        #ec_ui.ok_button.clicked.connect(lambda: self.update_open_event_config(ec_ui)
        ec_dialog.exec_()

    def update_open_event_config(self, ec_ui):
        text = ec_ui.comboBox.currentData
        ec_ui.label_3.setText(text)

    #Vector
    def add_vector(self):
        self.user_change = False
        self.table_manager.add_vector()
        self.table_manager.populate_vector_dropdowns(self.vc_vector_drop_down)
        self.table_manager.populate_vector_configuration_table()
        self.table_manager.populate_add_to_vector_table(self.lec_add_to_vector_table)
        self.user_change = True

    def rightClickLogEntry(self, point):
        index = self.lec_logentry_table.indexAt(point)

        if not index.isValid():
            return

        menu = QtWidgets.QMenu()
        menu.addAction("Show full description", self.log_entry_description_button_triggered)
        menu.exec_(self.lec_logentry_table.mapToGlobal(point))

    def log_table_clicked(self, item):
        if not self.user_change:
            return
        print("changing log table")
        if item.column() == 5:
            self.user_change = False
            self.ingest_funct.logFiles[item.row()].marked = not (item.checkState() == 0)

            if not (item.checkState() == 0):
                self.label_12.setText(self.ingest_funct.logFiles[item.row()].get_name())
                self.table_manager.populate_enforcement_action_report_table(self.ingest_funct.logFiles[item.row()])

            numlist = list(range(len(self.ingest_funct.logFiles)))
            numlist.remove(item.row())

            for i in numlist:
                self.ingest_funct.logFiles[i].marked = False
                self.tableWidget.setItem(i, 5, QTableWidgetItem(""))
                self.tableWidget.item(i, 5).setCheckState(QtCore.Qt.Unchecked)

            self.user_change = True

    def edit_table_log_entry(self, item):
        if not self.user_change:
            return
        self.user_change = False
        for i in range(self.lec_logentry_table.rowCount()):
            print("i is: ", i)
            if self.lec_logentry_table.item(i, 0).isSelected():
                self.lec_logentry_table.item(i, 0).setCheckState(item.checkState())

        self.user_change = True


    def edit_table_node(self, item):
        if not self.user_change:
            return
        if item.column() == 0:
            self.user_change = False
            self.table_manager.populate_node_table(self.vc_vector_drop_down.currentIndex())
            self.user_change = True
        elif item.column() == 9:
            self.table_manager.edit_node_table(item.row(), item.column(), (not item.checkState() == 0), self.vc_vector_drop_down.currentIndex())
        else:
            self.table_manager.edit_node_table(item.row(), item.column(), item.text(), self.vc_vector_drop_down.currentIndex())

    def edit_table_vector_configuration(self, item):
        if not self.user_change:
            return
        self.user_change = False
        if item.column() == 0:
            self.table_manager.edit_vector_table(item.row(), item.column(), (not item.checkState() == 0))
        else:
            self.table_manager.edit_vector_table(item.row(), item.column(), item.text())
        self.table_manager.populate_vector_dropdowns(self.vc_vector_drop_down)
        self.table_manager.populate_add_to_vector_table(self.lec_add_to_vector_table)
        self.user_change = True

    def resize_ui_components(self, PICK):
        self.set_column_widths_log_entry_tab()
        self.set_column_widths_event_tab()
        self.set_column_widths_vector_view_tab()

        self.button_connect_to_ip.clicked.connect(self.connect_button_triggered)
        self.nc_iconchange_button.clicked.connect(self.icon_edit_button_triggered)
        self.vc_push_button.clicked.connect(self.vector_db_button_triggered)
        self.vc_add_button.clicked.connect(self.createnode_button_triggered)
        self.lec_add_to_vector_button.clicked.connect(self.add_log_entry_to_vector)

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
                # graph(self.horizontalLayout_13).set_vector(manage_tables.vectors[i])

        self.table_manager.add_log_entries_to_vectors(selected_entries, self.splunk.logentries, selected_vectors)
        self.vector_dropdown_select()

        return

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
        # vnode_table_width = self.vc_node_table.width()
        vnode_table_width = 850
        vnode_table_width -= 5
        column_width = math.floor(vnode_table_width * .1)
        for i in range(0, 10):
            self.vc_node_table.setColumnWidth(i, column_width)

        # for Relationship Table
        # vrelationship_table_width = self.vc_relationship_table.width()
        vrelationship_table_width = 600
        vrelationship_table_width -= 5
        column_width = math.floor(vrelationship_table_width * .25)
        for i in range(0, 4):
            self.vc_relationship_table.setColumnWidth(i, column_width)

    def connect_button_triggered(self):
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

    def icon_edit_button_triggered(self):
        ic_dialog = QtWidgets.QDialog()
        ic_ui = UIIconConfigDialog()
        ic_ui.setupUi(ic_dialog)
        ic_dialog.exec_()

    def log_entry_description_button_triggered(self):
        ic_dialog = QtWidgets.QDialog()
        ic_ui = LogEntryDescription()
        ic_ui.setupUi(ic_dialog)
        ic_dialog.exec_()

    def vector_db_button_triggered(self):

        vdb_dialog = QtWidgets.QDialog()
        if self.checkBox_lead.isChecked():
            vdb_ui = UIVectorDBLead()
            vdb_ui.setupUi(vdb_dialog)
            vdb_ui.vdbcl_button_commit.clicked.connect(self.database.insert_vector)
        else:
            vdb_ui = UIVectorDBAnalyst()
            vdb_ui.setupUi(vdb_dialog)
            vdb_ui.vdbc_button_push.clicked.connect(self.database.insert_vector)
            vdb_ui.vdbc_button_pull.clicked.connect(self.database.update_vector)

        vdb_dialog.exec_()

        # db.__init__(self)

    def vector_dropdown_select(self):
        if not self.user_change:
            return
        self.user_change = False
        sel_vec = self.vc_vector_drop_down.currentIndex()
        print("Changed vector to: ", sel_vec)
        self.table_manager.populate_relationship_table(sel_vec)
        self.table_manager.populate_node_table(sel_vec)

        if sel_vec >= 0:
            self.vc_graph_widget.set_vector(self.table_manager.vectors[sel_vec])

        sel_vec = self.vc_vector_drop_down.currentIndex()
        self.vc_graph_widget.set_vector(self.table_manager.vectors[sel_vec])
        self.user_change = True

    def export_table_clicked(self, key):
        option = QFileDialog.Options()
        filename = QFileDialog.getSaveFileName(None, 'Export Graph', '', '"Csv (*.csv)"', options=option)
        if filename is not None:
            filename = str(filename[0])
            print("Exporting csv to: ", filename)
            switcher = {
                "log entry": lambda: self.table_manager.export_log_entry_table(filename=filename),
                "node": lambda: self.table_manager.export_node_table(self.vc_vector_drop_down.currentIndex(),
                                                                     filename=filename),
                "vector": lambda: self.table_manager.export_vector_configuration_table(filename=filename)}
            switcher[key]()

    def createnode_button_triggered(self):
        self.table_manager.create_node(self.vc_vector_drop_down.currentIndex())
        self.table_manager.populate_node_table(self.vc_vector_drop_down.currentIndex())
        sel_vec = self.vc_vector_drop_down.currentIndex()
        self.vc_graph_widget.set_vector(self.table_manager.vectors[sel_vec])
        # self.vc_graph_widget.set_vector(self.table_manager.vectors[sel_vec])

    def createrelationship_button_triggered(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = RelationshipDialog()
        ec_ui.setupUi(ec_dialog)
        self.table_manager.populate_node_dropdowns(self.vc_vector_drop_down.currentIndex(), ec_ui.child_id_combobox)
        self.table_manager.populate_node_dropdowns(self.vc_vector_drop_down.currentIndex(), ec_ui.parent_id_combobox)

        ec_ui.create_button.clicked.connect(lambda: self.create_relationship(
            self.vc_vector_drop_down.currentIndex(),
            ec_ui.parent_id_combobox.currentIndex(),
            ec_ui.child_id_combobox.currentIndex(),
            ec_ui.name_line_edit.text()
        ))
        ec_dialog.exec_()
        sel_vec = self.vc_vector_drop_down.currentIndex()
        self.vc_graph_widget.set_vector(self.table_manager.vectors[sel_vec])

    def create_relationship(self, selected_vector, parent_id, child_id, name):
        self.table_manager.create_relationship(
            selected_vector, parent_id=parent_id, child_id=child_id, name=name)
        # self.table_manager.create_relationship(self.vc_vector_drop_down.currentIndex())
        self.table_manager.populate_relationship_table(self.vc_vector_drop_down.currentIndex())
    
    #Open file directory when clicking button '...' in new Event Configuration
    def open_ingestion_directory_selector(self, textbox_widget=None, team=0):
        directory = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        if textbox_widget is None:
            print(directory)
        else:
            if team == 0:
                self.event_config.rootpath = str(directory)
            elif team == 1:
                self.event_config.redfolder = str(directory)
            elif team ==2:
                self.event_config.bluefolder = str(directory)
            elif team ==3:
                self.event_config.whitefolder = str(directory)
                
            textbox_widget.setPlainText(str(directory))
            # self.ingest_funct.ingest_directory_to_splunk(directory, self.event_config.name, self.splunk)

    def start_ingestion(self):
        self.ingest_funct.ingest_directory_to_splunk(self.event_config.rootpath, self.event_config.name, self.splunk)
        if self.event_config.redfolder == "":
            self.event_config.redfolder = self.event_config.rootpath+"/red"
        self.ingest_funct.ingest_directory_to_splunk(self.event_config.redfolder, self.event_config.name, self.splunk)
        if self.event_config.bluefolder == "":
            self.event_config.bluefolder = self.event_config.rootpath+"/blue"
        self.ingest_funct.ingest_directory_to_splunk(self.event_config.bluefolder, self.event_config.name, self.splunk)
        if self.event_config.whitefolder == "":
            self.event_config.whitefolder = self.event_config.rootpath+"/white"
        self.ingest_funct.ingest_directory_to_splunk(self.event_config.whitefolder, self.event_config.name, self.splunk)

    def update_tables_periodically(self):
        self.splunk.get_log_count(bypass_check=True)
        self.table_manager.populate_logentry_table(self.splunk.logentries)
        while True:
            time.sleep(10)
            change = self.splunk.get_log_count()
            print("Update check")
            if change == 1:
                self.user_change = False
                self.table_manager.populate_logentry_table(self.splunk.logentries)
                self.user_change = True

    def connect_lead_triggered(self):
        if self.checkBox_lead.isChecked():
            ec_dialog = QtWidgets.QDialog()
            ec_ui = SPLUNKLoginDialog()
            ec_ui.setupUi(ec_dialog)
            ec_ui.push_button_connect.clicked.connect(lambda: self.connect_lead(ec_ui))
            ec_ui.push_button_cancel.clicked.connect(lambda: self.checkBox_lead.setCheckState(QtCore.Qt.Unchecked))
            ec_dialog.exec_()
        else:
            print("lead unchecked, must disconnect")

    def connect_lead(self, ec_ui):
        print("Connecting client to Splunk ...")
        if self.splunk.connect_client(ec_ui.line_edit_username.text(), ec_ui.line_edit_password.text()):
            # Starts auto-refresh logs thread
            thread = threading.Thread(target=self.update_tables_periodically)
            thread.start()
        else:
            print("Splunk connection failed")
            self.checkBox_lead.setCheckState(QtCore.Qt.Unchecked)



if __name__ == "__main__":
    app = QApplication([])
    PICK = QtWidgets.QMainWindow()
    path = QtGui.QPainterPath()
    scene = QtWidgets.QGraphicsScene()
    ui = functionality()
    ui.setupUi(PICK)
    PICK.show()
    ui.resize_ui_components(PICK)
    sys.exit(app.exec_())
