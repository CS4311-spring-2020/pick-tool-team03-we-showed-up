# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icon_Configuration_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(579, 454)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.icon_configBox = QtWidgets.QGroupBox(Dialog)
        self.icon_configBox.setMinimumSize(QtCore.QSize(351, 70))
        self.icon_configBox.setMaximumSize(QtCore.QSize(16777215, 70))
        self.icon_configBox.setAutoFillBackground(True)
        self.icon_configBox.setObjectName("icon_configBox")
        self.icon_addIcon = QtWidgets.QPushButton(self.icon_configBox)
        self.icon_addIcon.setGeometry(QtCore.QRect(20, 30, 89, 25))
        self.icon_addIcon.setObjectName("icon_addIcon")
        self.icon_deleteIcon = QtWidgets.QPushButton(self.icon_configBox)
        self.icon_deleteIcon.setGeometry(QtCore.QRect(130, 30, 89, 25))
        self.icon_deleteIcon.setObjectName("icon_deleteIcon")
        self.icon_editIcon = QtWidgets.QPushButton(self.icon_configBox)
        self.icon_editIcon.setGeometry(QtCore.QRect(240, 30, 89, 25))
        self.icon_editIcon.setObjectName("icon_editIcon")
        self.verticalLayout.addWidget(self.icon_configBox)
        self.IconTable = QtWidgets.QTableWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IconTable.sizePolicy().hasHeightForWidth())
        self.IconTable.setSizePolicy(sizePolicy)
        self.IconTable.setMinimumSize(QtCore.QSize(500, 300))
        self.IconTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.IconTable.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.IconTable.setAutoFillBackground(True)
        self.IconTable.setObjectName("IconTable")
        self.IconTable.setColumnCount(4)
        self.IconTable.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked)
        self.IconTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked)
        self.IconTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked)
        self.IconTable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(2, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked)
        self.IconTable.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(3, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked)
        self.IconTable.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(4, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked)
        self.IconTable.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(5, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.IconTable.setItem(5, 3, item)
        self.IconTable.horizontalHeader().setCascadingSectionResizes(True)
        self.IconTable.horizontalHeader().setDefaultSectionSize(130)
        self.IconTable.horizontalHeader().setMinimumSectionSize(130)
        self.IconTable.horizontalHeader().setSortIndicatorShown(True)
        self.verticalLayout.addWidget(self.IconTable)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.icon_configBox.setTitle(_translate("Dialog", "Icon Configuration"))
        self.icon_addIcon.setText(_translate("Dialog", "Add Icon"))
        self.icon_deleteIcon.setText(_translate("Dialog", "Delete Icon"))
        self.icon_editIcon.setText(_translate("Dialog", "Edit Icon"))
        item = self.IconTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Icon Name"))
        item = self.IconTable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Icon Source"))
        item = self.IconTable.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Image Preview"))
        __sortingEnabled = self.IconTable.isSortingEnabled()
        self.IconTable.setSortingEnabled(False)
        item = self.IconTable.item(0, 1)
        item.setText(_translate("Dialog", "initial_state"))
        item = self.IconTable.item(0, 2)
        item.setText(_translate("Dialog", "emojipedia.org"))
        item = self.IconTable.item(0, 3)
        item.setText(_translate("Dialog", "🔴 "))
        item = self.IconTable.item(1, 1)
        item.setText(_translate("Dialog", "start_state"))
        item = self.IconTable.item(1, 2)
        item.setText(_translate("Dialog", "emojipedia.org"))
        item = self.IconTable.item(1, 3)
        item.setText(_translate("Dialog", "🔵"))
        item = self.IconTable.item(2, 1)
        item.setText(_translate("Dialog", "attack_state"))
        item = self.IconTable.item(2, 2)
        item.setText(_translate("Dialog", "emojipedia.org"))
        item = self.IconTable.item(2, 3)
        item.setText(_translate("Dialog", "🌀"))
        item = self.IconTable.item(3, 1)
        item.setText(_translate("Dialog", "verify_state"))
        item = self.IconTable.item(3, 2)
        item.setText(_translate("Dialog", "emojipedia.org"))
        item = self.IconTable.item(3, 3)
        item.setText(_translate("Dialog", "⭕"))
        item = self.IconTable.item(4, 1)
        item.setText(_translate("Dialog", "clear_state"))
        item = self.IconTable.item(4, 2)
        item.setText(_translate("Dialog", "emojipedia.org"))
        item = self.IconTable.item(4, 3)
        item.setText(_translate("Dialog", "💬"))
        item = self.IconTable.item(5, 1)
        item.setText(_translate("Dialog", "ready_state"))
        item = self.IconTable.item(5, 2)
        item.setText(_translate("Dialog", "emojipedia.org"))
        item = self.IconTable.item(5, 3)
        item.setText(_translate("Dialog", "✅"))
        self.IconTable.setSortingEnabled(__sortingEnabled)
