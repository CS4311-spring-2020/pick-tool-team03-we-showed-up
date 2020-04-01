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
        colors = ["red", "white", "blue", "red", "blue", "white", "red", "blue", "white"]
        super(Path, self).__init__(path)
        for i in range(path.elementCount()):
            node = Node(self, i)
            node.setPos(QPointF(path.elementAt(i)))
            node_name = "node " + str(i + 1)
            node.setBrush(QBrush(QColor(colors[i])))
            text = QGraphicsSimpleTextItem(node_name)
            text.setParentItem(node)
            text.setPen(QPen(QPen(QColor("black"))))
            scene.addItem(node)
        self.setPen(QtGui.QPen(Qt.black, 1.75))

    def updateElement(self, index, pos):
        path.setElementPositionAt(index, pos.x(), pos.y())
        self.setPath(path)