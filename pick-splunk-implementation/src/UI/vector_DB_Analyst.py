# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vector_DB_Analyst.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(911, 344)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.vdb_label_connectheader = QtWidgets.QLabel(Dialog)
        self.vdb_label_connectheader.setMaximumSize(QtCore.QSize(16777215, 25))
        self.vdb_label_connectheader.setObjectName("vdb_label_connectheader")
        self.verticalLayout_3.addWidget(self.vdb_label_connectheader)
        self.vdbc_label_connection = QtWidgets.QLabel(Dialog)
        self.vdbc_label_connection.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.vdbc_label_connection.setFont(font)
        self.vdbc_label_connection.setObjectName("vdbc_label_connection")
        self.verticalLayout_3.addWidget(self.vdbc_label_connection)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vdbc_table_pulledvectortable = QtWidgets.QTableWidget(self.groupBox)
        self.vdbc_table_pulledvectortable.setObjectName("vdbc_table_pulledvectortable")
        self.vdbc_table_pulledvectortable.setColumnCount(4)
        self.vdbc_table_pulledvectortable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.vdbc_table_pulledvectortable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbc_table_pulledvectortable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbc_table_pulledvectortable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbc_table_pulledvectortable.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.vdbc_table_pulledvectortable)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.vdbc_button_pull = QtWidgets.QPushButton(self.groupBox)
        self.vdbc_button_pull.setObjectName("vdbc_button_pull")
        self.horizontalLayout.addWidget(self.vdbc_button_pull)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vdbc_table_pushedvector = QtWidgets.QTableWidget(self.groupBox_2)
        self.vdbc_table_pushedvector.setObjectName("vdbc_table_pushedvector")
        self.vdbc_table_pushedvector.setColumnCount(4)
        self.vdbc_table_pushedvector.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.vdbc_table_pushedvector.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbc_table_pushedvector.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbc_table_pushedvector.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbc_table_pushedvector.setHorizontalHeaderItem(3, item)
        self.verticalLayout_2.addWidget(self.vdbc_table_pushedvector)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.vdbc_button_push = QtWidgets.QPushButton(self.groupBox_2)
        self.vdbc_button_push.setObjectName("vdbc_button_push")
        self.horizontalLayout_2.addWidget(self.vdbc_button_push)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.vdb_label_connectheader.setText(_translate("Dialog", "Connection Status to Lead:"))
        self.vdbc_label_connection.setText(_translate("Dialog", "Connected"))
        self.groupBox.setTitle(_translate("Dialog", "Pulled Vector DB Table (Analyst)"))
        item = self.vdbc_table_pulledvectortable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Vector"))
        item = self.vdbc_table_pulledvectortable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Description"))
        item = self.vdbc_table_pulledvectortable.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Status"))
        self.pushButton.setText(_translate("Dialog", "Sync"))
        self.vdbc_button_pull.setText(_translate("Dialog", "Pull"))
        self.groupBox_2.setTitle(_translate("Dialog", "Pushed Vector DB Table (Analyst)"))
        item = self.vdbc_table_pushedvector.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Vector"))
        item = self.vdbc_table_pushedvector.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Description"))
        item = self.vdbc_table_pushedvector.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Push Status"))
        self.pushButton_2.setText(_translate("Dialog", "Sync"))
        self.vdbc_button_push.setText(_translate("Dialog", "Push"))

