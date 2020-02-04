import math

from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from mainwindow import Ui_PICK
from IP_Error_ConnectionLimitReached import Ui_Dialog as ui_connection_limit
from IP_Error_duplicateLeadIP import Ui_Dialog as ui_duplicate_lead_ip
from IP_Error_LeadIPBoxSelected import Ui_Dialog as ui_lead_ip_selected
from IP_Error_LeadIPNotProvided import Ui_Dialog as ui_lead_ip_not_provided
from icon_Configuration_Dialog import Ui_Dialog as ui_icon_config_dialog

import sys

rad = 20


# class mywindow(QtWidgets.QMainWindow):

#     def __init__(self):

#         super(mywindow, self).__init__()

#         self.ui = Ui_PICK()

#         self.ui.setupUi(self)

#         self.ui.label.setFont(QtGui.QFont('SansSerif', 30)) # change font type and size

class functionality(Ui_PICK):
    def setupUi(self, PICK):
        super().setupUi(PICK)
        self.vc_search_box.setPlainText("hello")

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

    def add_node(self):
        import random
        path.lineTo(random.randint(50, 300), random.randint(50, 300));
        scene.addItem(Path(path, scene))

    def resize_ui_components(self, PICK):
        self.set_column_widths_log_entry_tab()
        self.set_column_widths_event_tab()
        self.set_column_widths_vector_view_tab()

        self.button_connect_to_ip.clicked.connect(self.connect_button_triggered)
        # self.button_connect_to_ip.clicked.connect(self.icon_edit_button_triggered)

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
            bt_ui = ui_duplicate_lead_ip()
            bt_ui.setupUi(bt_dialog)
            bt_ui.pushButton.clicked.connect(bt_dialog.close)
            bt_dialog.exec_()

        elif self.textbox_ip.toPlainText() == "":
            print("no lead ip error prompt")
            bt_ui = ui_lead_ip_not_provided()
            bt_ui.setupUi(bt_dialog)
            bt_ui.pushButton.clicked.connect(bt_dialog.close)
            bt_dialog.exec_()

        elif self.checkBox_lead.isChecked():
            print("lead checked error prompt")
            bt_ui = ui_lead_ip_selected()
            bt_ui.setupUi(bt_dialog)
            bt_ui.pushButton.clicked.connect(bt_dialog.close)
            bt_dialog.exec_()

        elif no_connections > 20:
            print("max connections error prompt")
            bt_ui = ui_connection_limit()
            bt_ui.setupUi(bt_dialog)
            bt_ui.pushButton.clicked.connect(bt_dialog.close)
            bt_dialog.exec_()

        else:
            print("successful connection should take place.")

    def icon_edit_button_triggered(self):
        ic_dialog = QtWidgets.QDialog()
        ic_ui = ui_icon_config_dialog()
        ic_ui.setupUi(ic_dialog)
        ic_dialog.exec_()



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
