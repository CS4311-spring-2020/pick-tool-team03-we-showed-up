# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Create_Relationship_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 179)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 28))
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.name_line_edit = QtWidgets.QLineEdit(Dialog)
        self.name_line_edit.setMaximumSize(QtCore.QSize(16777215, 28))
        self.name_line_edit.setObjectName("name_line_edit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_line_edit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.parent_id_combobox = QtWidgets.QComboBox(Dialog)
        self.parent_id_combobox.setObjectName("parent_id_combobox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.parent_id_combobox)
        self.child_id_combobox = QtWidgets.QComboBox(Dialog)
        self.child_id_combobox.setObjectName("child_id_combobox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.child_id_combobox)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setMaximumSize(QtCore.QSize(60, 28))
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.create_button = QtWidgets.QPushButton(Dialog)
        self.create_button.setMaximumSize(QtCore.QSize(80, 28))
        self.create_button.setObjectName("create_button")
        self.horizontalLayout.addWidget(self.create_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_4.setText(_translate("Dialog", "Create a Node Relationship:"))
        self.label.setText(_translate("Dialog", "Name:"))
        self.label_2.setText(_translate("Dialog", "Parent ID:"))
        self.label_3.setText(_translate("Dialog", "Child ID:"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.create_button.setText(_translate("Dialog", "Create"))

        self.create_button.clicked.connect(Dialog.accept)
        self.cancel_button.clicked.connect(Dialog.reject)
        self.cancel_button.setDefault(False)
        self.cancel_button.setAutoDefault(False)

