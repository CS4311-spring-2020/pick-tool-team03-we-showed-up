import math

from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from mainwindow import Ui_PICK
from choose_Vector_Screen import Ui_Dialog as UI_ChooseVector
from IP_Error_ConnectionLimitReached import Ui_Dialog as UIConnectionLimit
from IP_Error_duplicateLeadIP import Ui_Dialog as UIDuplicateLeadIP
from IP_Error_LeadIPBoxSelected import Ui_Dialog as UILeadIPSelected
from IP_Error_LeadIPNotProvided import Ui_Dialog as UILeadIPNotProvided
from icon_Configuration_Dialog import Ui_Dialog as UIIconConfigDialog
from vector_DB_Lead import Ui_Dialog as UIVectorDBLead
from vector_DB_Analyst import Ui_Dialog as UIVectorDBAnalyst
from manage_tables import manage_tables
from SPLUNKInterface import SPLUNKInterface
from logentrydescription import Ui_Dialog as LogEntryDescription
from EventConfigurationNew import Ui_Dialog as UiEventConfigNew
from EventConfigurationOpen import Ui_Dialog as UiEventConfigOpen
from EventConfigurationEdit import Ui_Dialog as UiEventConfigEdit
from ingestion_functionality import IngestionFunctionality as Ingest
from eventconfiguration import EventConfiguration

import sys
import threading
import time

rad = 20


# class mywindow(QtWidgets.QMainWindow):

#     def __init__(self):

#         super(mywindow, self).__init__()

#         self.ui = Ui_PICK()

#         self.ui.setupUi(self)

#         self.ui.label.setFont(QtGui.QFont('SansSerif', 30)) # change font type and size

class functionality(Ui_PICK):
    table_manager = manage_tables()
    splunk = SPLUNKInterface()
    user_change = True
    event_config = EventConfiguration()
    event_config.name = "main"
    ingest_funct = Ingest()

    def setupUi(self, PICK):
        super().setupUi(PICK)
        path.moveTo(0, 0)
        # path.cubicTo(-30, 70, 35, 115, 100, 100);
        path.lineTo(200, 100);
        path.lineTo(100, 100);
        path.lineTo(100, 200);
        # path.cubicTo(200, 30, 150, -35, 60, -30);

        scene.addItem(Path(path, scene))

        self.vc_graph_view.setScene(scene)
        # view = QGraphicsView(scene)
        # view.setRenderHint(QtGui.QPainter.Antialiasing)
        # view.resize(600, 400)
        # view.show()
        # app.exec_()

        self.vc_add_button.clicked.connect(self.add_node)
        self.table_manager.populate_lfc_table(self.tableWidget)
        self.table_manager.populate_logentry_table(self.lec_logentry_table, self.splunk.logentries)
        self.table_manager.populate_relationship_table(self.vc_relationship_table, 0)
        self.table_manager.populate_vector_table(self.vc_node_table, 0)
        self.table_manager.populate_vectorconfiguration_table(self.vc_table)
        self.table_manager.populate_enforcementactionreports_table(self.tableWidget_2, 0)
        self.table_manager.populate_vector_dropdowns(self.vc_vector_drop_down)
        self.vc_vector_drop_down.currentIndexChanged.connect(self.vector_dropdown_select)
        self.button_add_vector.clicked.connect(self.add_vector)
        self.vc_add_relationship_button.clicked.connect(self.createrelationship_button_triggered)


        self.lec_logentry_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.lec_logentry_table.customContextMenuRequested.connect(self.rightClickLogEntry)
        # Open file directory when clicking button 'export' in vector view
        self.nc_export_button.clicked.connect(self.export_vector)
        self.ec_export_button.clicked.connect(self.export_graph)
        self.vc_export_pushButton.clicked.connect(self.export_graph)
        self.log_file_export_pushButton.clicked.connect(self.export_graph)
        self.ear_export_pushButton.clicked.connect(self.export_graph)
        self.tableWidget.itemChanged.connect(self.printItemChanged)
        self.vc_node_table.itemChanged.connect(self.edit_table_node)

        # SPLUNK
        self.actionNew.triggered.connect(self.open_new_event_config)
        self.actionOpen.triggered.connect(self.open_events_config)
        self.actionEdit.triggered.connect(self.edit_event_config)

        thread = threading.Thread(target=self.update_tables_periodically)
        thread.start()
        # SPLUNK WEIRD AF, DO NOT TOUCH

    #SPLUNK - New Event
    def open_new_event_config(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = UiEventConfigNew()
        ec_ui.setupUi(ec_dialog)
        ec_ui.button_save_event.clicked.connect(lambda: self.call_create_index(ec_ui))
        ec_ui.button_start_ingestion.clicked.connect(lambda: self.start_ingestion(ec_ui))
        #save directories of teams
        ec_ui.root_directory_pushButton.clicked.connect(lambda: self.openDirectorySelector(ec_ui.textbox_root_directory))
        ec_ui.red_team_directory_pushButton.clicked.connect(lambda: self.openDirectorySelector(ec_ui.textbox_red_team_folder))
        ec_ui.blue_team_directory_pushButton.clicked.connect(lambda: self.openDirectorySelector(ec_ui.textbox_blue_team_folder))
        ec_ui.white_team_directory_pushButton.clicked.connect(lambda: self.openDirectorySelector(ec_ui.textbox_white_team_folder))
        ec_dialog.exec_()

    def call_create_index(self, ec_ui):
        event_name = ec_ui.textbox_event_name.toPlainText()
        event_description = ec_ui.textbox_event_description.toPlainText()
        flag = self.splunk.createEvent(event_name, event_description)
        if flag == 1:
            ec_ui.event_creation_status_label.setText("Sorry, event name is taken.")
        else:
            text = "Event " + event_name + " added."
            self.event_config.name = event_name
            ec_ui.event_creation_status_label.setText(text)

    def start_ingestion(self, ec_ui):
        red_path = ec_ui.textbox_red_team_folder.toPlainText()
        blue_path = ec_ui.textbox_blue_team_folder.toPlainText()
        white_path = ec_ui.textbox_white_team_folder.toPlainText()
        root_path = ec_ui.textbox_root_directory.toPlainText()
        self.splunk.addFilesMonitorDirectory(red_team_path, blue_team_path, white_team_path, root_path)

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

    #SPLUNK - Edit Event
    def edit_event_config(self):
        ec_dialog = QtWidgets.QDialog()
        ec_ui = UiEventConfigEdit()
        ec_ui.setupUi(ec_dialog)
        events = self.splunk.getIndexList()
        for event in events:
            ec_ui.comboBox.addItem(event)
        ec_ui.button_save_event.clicked.connect
        ec_dialog.exec_()

    #Vector
    def add_vector(self):
        self.table_manager.add_vector()
        self.table_manager.populate_vector_dropdowns(self.vc_vector_drop_down)
        self.table_manager.populate_vectorconfiguration_table(self.vc_table)

    def rightClickLogEntry(self, point):
        index = self.lec_logentry_table.indexAt(point)

        if not index.isValid():
            return

        menu = QtWidgets.QMenu()
        menu.addAction("Add to vector", self.showVectorOptions)
        menu.addAction("Show full description", self.log_entry_description_button_triggered)
        menu.exec_(self.lec_logentry_table.mapToGlobal(point))

    def showVectorOptions(self):
        self.ui_svo = UI_ChooseVector()
        self.ui_svo.setupUi(vector_dialog)
        self.table_manager.populate_vector_dropdowns(self.ui_svo.comboBox)
        vector_dialog.exec_()

    def add_node(self):
        import random
        path.lineTo(random.randint(50, 300), random.randint(50, 300))
        scene.addItem(Path(path, scene))

    def printItemChanged(self, item):
        print("item changed row:", item.row(), " column: ", item.column())

    def edit_table_node(self, item):
        if not self.user_change:
            return
        print("changing table")
        if item.column() == 0:
            self.user_change = False
            self.table_manager.populate_vector_table(self.vc_node_table, self.vc_vector_drop_down.currentIndex())
            self.user_change = True
        elif item.column() == 9:
            if item.checkState() == 0:
                self.table_manager.edit_node_table(item.row(), item.column(), False, self.vc_vector_drop_down.currentIndex())
            else:
                self.table_manager.edit_node_table(item.row(), item.column(), True, self.vc_vector_drop_down.currentIndex())
        else:
            self.table_manager.edit_node_table(item.row(), item.column(), item.text(), self.vc_vector_drop_down.currentIndex())

    def resize_ui_components(self, PICK):
        self.set_column_widths_log_entry_tab()
        self.set_column_widths_event_tab()
        self.set_column_widths_vector_view_tab()

        self.button_connect_to_ip.clicked.connect(self.connect_button_triggered)
        self.nc_iconchange_button.clicked.connect(self.icon_edit_button_triggered)
        self.vc_push_button.clicked.connect(self.vector_db_button_triggered)
        self.vc_add_button.clicked.connect(self.createnode_button_triggered)

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
        else:
            vdb_ui = UIVectorDBAnalyst()
        vdb_ui.setupUi(vdb_dialog)
        vdb_dialog.exec_()

    def vector_dropdown_select(self):
        self.user_change = False
        sel_vec = self.vc_vector_drop_down.currentIndex()
        print("Changed vector to: ", sel_vec)
        self.table_manager.populate_relationship_table(self.vc_relationship_table, sel_vec)
        self.table_manager.populate_vector_table(self.vc_node_table, sel_vec)
        self.user_change = True

    #Open file directory when clicking button 'export' in vector view
    def export_graph(self):
        self.openSaveDialog()

    def export_vector(self):
        print(self.openSaveDialog())

    def openSaveDialog(self):
        option = QFileDialog.Options()
        filename = QFileDialog.getSaveFileName(None, 'Export Graph', '', '"CSV (*.csv)"', options=option)
        filename = str(filename[0])
        self.table_manager.export_table_to_csv( self.table_manager.fake_data.vector_list[0].nodes, filename=filename)

    def createnode_button_triggered(self):
        self.table_manager.create_node(self.vc_vector_drop_down.currentIndex())
        self.table_manager.populate_vector_table(self.vc_node_table, self.vc_vector_drop_down.currentIndex())

    def createrelationship_button_triggered(self):
        self.table_manager.create_relationship(self.vc_vector_drop_down.currentIndex())
        self.table_manager.populate_relationship_table(self.vc_relationship_table, self.vc_vector_drop_down.currentIndex())
    
    #Open file directory when clicking button '...' in new Event Configuration
    def openDirectorySelector(self, textbox_widget=None):
        directory = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        if textbox_widget is None:
            print(directory)
        else:
            textbox_widget.setPlainText(str(directory))
            self.ingest_funct.ingest_directory_to_splunk(directory, self.event_config.name, self.splunk)
            # Ingest.get_file_paths_from_folder(str(directory))

    def update_tables_periodically(self):
        while True:
            time.sleep(20)
            change = self.splunk.get_log_count()
            print("Should UPDATE NOW")
            if change == 1:
                self.splunk.refresh_log_entries()
                self.table_manager.populate_logentry_table(self.lec_logentry_table, self.splunk.logentries)

class Node(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, path, index):
        super(Node, self).__init__(-rad, -rad, 2 * rad, 2 * rad)

        self.rad = rad
        self.path = path
        self.index = index

        self.setZValue(1)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(Qt.white)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            self.path.updateElement(self.index, value.toPoint())
        return QtWidgets.QGraphicsEllipseItem.itemChange(self, change, value)


class Path(QtWidgets.QGraphicsPathItem):
    def __init__(self, path, scene):
        super(Path, self).__init__(path)
        for i in range(path.elementCount()):
            node = Node(self, i)
            node.setPos(QPointF(path.elementAt(i)))
            scene.addItem(node)
        self.setPen(QtGui.QPen(Qt.black, 1.75))

    def updateElement(self, index, pos):
        path.setElementPositionAt(index, pos.x(), pos.y())
        self.setPath(path)


# app = QtWidgets.QApplication([])

# application = mywindow()

# application.show()

# sys.exit(app.exec())

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
