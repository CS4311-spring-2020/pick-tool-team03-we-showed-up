from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
 
from mainwindow import Ui_PICK
 
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
        
        path.moveTo(0,0)
        #path.cubicTo(-30, 70, 35, 115, 100, 100);
        path.lineTo(200, 100);
        path.lineTo(100, 100);
        path.lineTo(100, 200);
        #path.cubicTo(200, 30, 150, -35, 60, -30);

        
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
        path.lineTo(random.randint(50,300), random.randint(50,300));
        scene.addItem(Path(path, scene))


class Node(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, path, index):
        super(Node, self).__init__(-rad, -rad, 2*rad, 2*rad)

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
    sys.exit(app.exec_())


