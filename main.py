# This Python file uses the following encoding: utf-8
import sys
#from PySide2.QtWidgets import QApplication
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = uic.loadUi("mainwindow.ui")
    window.show()
    sys.exit(app.exec_())
