# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vector_DB_Lead.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(777, 428)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vdbcl_table_approvalsynctable = QtWidgets.QTableWidget(self.groupBox)
        self.vdbcl_table_approvalsynctable.setObjectName("vdbcl_table_approvalsynctable")
        self.vdbcl_table_approvalsynctable.setColumnCount(7)
        self.vdbcl_table_approvalsynctable.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.vdbcl_table_approvalsynctable.setHorizontalHeaderItem(6, item)
        self.verticalLayout.addWidget(self.vdbcl_table_approvalsynctable)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.vdbcl_button_commit = QtWidgets.QPushButton(self.groupBox)
        self.vdbcl_button_commit.setMaximumSize(QtCore.QSize(16777215, 26))
        self.vdbcl_button_commit.setObjectName("vdbcl_button_commit")
        self.horizontalLayout.addWidget(self.vdbcl_button_commit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Approval Sync"))
        item = self.vdbcl_table_approvalsynctable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Source IP"))
        item = self.vdbcl_table_approvalsynctable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Request Timestamp"))
        item = self.vdbcl_table_approvalsynctable.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Vector"))
        item = self.vdbcl_table_approvalsynctable.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Description"))
        item = self.vdbcl_table_approvalsynctable.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Change Summary"))
        item = self.vdbcl_table_approvalsynctable.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "Sync Status"))
        self.vdbcl_button_commit.setText(_translate("Dialog", "Commit"))

