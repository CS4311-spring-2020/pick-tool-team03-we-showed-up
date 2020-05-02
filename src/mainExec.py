import sys

from main import functionality as UIFunctionality
from EventConfiguration import EventConfiguration
from IngestionFunctionality import IngestionFunctionality
from SPLUNKInterface import SPLUNKInterface
from TableManager import TableManager as TableManager
from Connections.Network import Network
from UndoRedoManager import UndoRedoManager

from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

if __name__ == "__main__":
    event_config = EventConfiguration(name="main")
    splunk = SPLUNKInterface(event_config=event_config)
    table_manager = TableManager()
    undo_redo_manager = UndoRedoManager(table_manager=table_manager)
    network = Network()
    ingestion = IngestionFunctionality(splunk=splunk, table_manager=table_manager, event_config=event_config)
    ui_f = UIFunctionality(table_manager=table_manager, splunk=splunk,
                           ingest_funct=ingestion, event_config=event_config, network=network)

    app = QApplication([])
    PICK = QtWidgets.QMainWindow()
    ui = ui_f
    ui.setupUi(PICK)
    PICK.show()
    ui.resize_ui_components(PICK)
    sys.exit(app.exec_())
