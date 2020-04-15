# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SPLUNK_Login_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 168)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QtWidgets.QLabel(Dialog)
        self.title_label.setMaximumSize(QtCore.QSize(16777215, 25))
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_username = QtWidgets.QLabel(Dialog)
        self.label_username.setObjectName("label_username")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_username)
        self.label_password = QtWidgets.QLabel(Dialog)
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.line_edit_username = QtWidgets.QLineEdit(Dialog)
        self.line_edit_username.setObjectName("line_edit_username")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.line_edit_username)
        self.line_edit_password = QtWidgets.QLineEdit(Dialog)
        self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_password.setObjectName("line_edit_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.line_edit_password)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.push_button_cancel = QtWidgets.QPushButton(Dialog)
        self.push_button_cancel.setMaximumSize(QtCore.QSize(60, 25))
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.horizontalLayout.addWidget(self.push_button_cancel)
        self.push_button_connect = QtWidgets.QPushButton(Dialog)
        self.push_button_connect.setMaximumSize(QtCore.QSize(80, 25))
        self.push_button_connect.setObjectName("push_button_connect")
        self.horizontalLayout.addWidget(self.push_button_connect)
        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "SPLUNK Login"))
        self.title_label.setText(_translate("Dialog", "Connect to SPLUNK"))
        self.label_username.setText(_translate("Dialog", "Username:"))
        self.label_password.setText(_translate("Dialog", "Password:"))
        self.push_button_cancel.setText(_translate("Dialog", "Cancel"))
        self.push_button_connect.setText(_translate("Dialog", "Connect"))

        self.push_button_connect.clicked.connect(Dialog.accept)
        self.push_button_cancel.clicked.connect(Dialog.reject)
