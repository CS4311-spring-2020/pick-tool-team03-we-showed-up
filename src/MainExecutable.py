import sys
from MainUI import UIMain
from EventConfiguration import EventConfiguration
from IngestionManager import IngestionManager
from SPLUNKInterface import SPLUNKInterface
from TableManager import TableManager as TableManager
from Connections.Network import Network
from UndoRedoManager import UndoRedoManager
from Controller import Controller
from EventSession import EventSession
from Connections.Database import Database
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

if __name__ == "__main__":

    event_config = EventConfiguration(name="main")
    event_session = EventSession(event_config=event_config)
    splunk = SPLUNKInterface(event_session=event_session)
    table_manager = TableManager()
    undo_manager = UndoRedoManager(table_manager=table_manager, event_session=event_session)
    table_manager.undo_manager = undo_manager
    network = Network()
    db = Database()
    ingestion = IngestionManager(splunk=splunk, table_manager=table_manager, event_session=event_session)
    controller = Controller(event_session=event_session,
                            table_manager=table_manager,
                            splunk=splunk,
                            ingestion=ingestion,
                            db=db,
                            undo_manager=undo_manager)
    ui_f = UIMain(table_manager=table_manager,
                  event_session=event_session,
                  network=network,
                  controller=controller,
                  undo_manager=undo_manager)

    app = QApplication([])
    PICK = QtWidgets.QMainWindow()
    ui = ui_f
    ui.setupUi(PICK)
    PICK.show()
    ui.resize_ui_components(PICK)
    sys.exit(app.exec_())
