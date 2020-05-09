from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QPushButton, QInputDialog, QLineEdit, QLabel
from QGraphViz.QGraphViz import QGraphViz, QGraphVizManipulationMode
from QGraphViz.DotParser import Graph, GraphType
from QGraphViz.Engines import Dot

 
class GraphInterface(QWidget):
    
    qgv = ""

    # initializing first instances of vector and QGraphViz aka qgv
    def __init__(self, layout, vector=None):
        self.vector = vector
        self.qgv = self.create_QGraphViz()
        self.layout_u = layout
        self.read_vector_table(vector)
 
    # refreshes the qgv every time a change in the nodes or relationships is made
    def set_vector(self, vector):
        if not self.vector == vector:
            self.vector = vector
        self.qgv = self.create_QGraphViz()
        self.update_graph(vector)

    # checks if there is information in the node and relationship tables
    # and either displays an empty graph or calls update_graph() if there are elements in the tables
    def read_vector_table(self, vector):
        if(vector == None):
            qgv = self.qgv
            show_subgraphs=True
            qgv.setStyleSheet("background-color:white;")
            # Create A new Graph using Dot layout engine
            qgv.new(Dot(Graph("Main_Graph"), show_subgraphs=show_subgraphs))
            
            # Define some graph
            n1 = qgv.addNode(qgv.engine.graph, "Node1", label="Nothing to show", fillcolor="white")
 

            # Build the graph (the layout engine organizes where the nodes and connections are)
            qgv.build()
            # Save it to a file to be loaded by Graphviz if needed
            qgv.save("./gv/test.gv")
 
            # Add the QGraphViz object to the layout
            self.layout_u.addWidget(qgv)
            self.qgv = qgv
        else:
            self.update_graph(vector)

    # creates initial empty graph and reads node and relationship tables every time there is a change
    # creates graphical elements for all nodes and edges
    def update_graph(self,vector):
        show_subgraphs=True
        
        qgv =self.qgv
        show_subgraphs=True
        qgv.setStyleSheet("background-color:white;")
        # Create A new Graph using Dot layout engine
        qgv.new(Dot(Graph("Main_Graph"), show_subgraphs=show_subgraphs))

        vector_name = vector.name
        
        # destroys previous graph so it can be populated by the new elements
        if((self.layout_u.count())>0):
                while self.layout_u.count():
                    child = self.layout_u.takeAt(0)
                    if child.widget() :
                        child.widget().deleteLater()
                 
        node_dict = {}
        # reads node info and creates graphical nodes
        for i in range(len(vector.get_nodes())):
            if vector.get_nodes()[i].is_visible():
                node_name = (vector.get_nodes()[i].get_name())
                node_type = (vector.get_nodes()[i].get_log_creator())

                if node_type == 'red' or node_type == 'blue' or node_type == "white":
                    color = node_type

                else:
                    color = "grey"
                node_dict[str(vector.get_nodes()[i].get_id())] = self.qgv.addNode(qgv.engine.graph, node_name, label=node_name, fillcolor=color)
                # n.append(self.qgv.addNode(qgv.engine.graph, node_name, label=node_name, fillcolor=color))

        # reads relationship information and creates lines between nodes
        for i in range(len(vector.get_relationships())):
            if vector.get_relationships()[i].parent.is_visible() and vector.get_relationships()[i].child.is_visible():
                # parent_node = n[int(vector.get_relationships()[i].get_parent_id())-1]
                # child_node = n[int(vector.get_relationships()[i].get_child_id())-1]
                parent_node = node_dict[str(vector.get_relationships()[i].get_parent_id())]
                child_node = node_dict[str(vector.get_relationships()[i].get_child_id())]
                self.qgv.addEdge(parent_node, child_node, {})
          
        # builds new graph, saves it in a qgv file, and loads it back onto the widget
            
        qgv.build()
        
        for i in range(len(vector.get_nodes())):
            if vector.get_nodes()[i].x != 0 and vector.get_nodes()[i].is_visible():
                node_dict[vector.get_nodes()[i].get_id()].pos[0] = vector.get_nodes()[i].x
                node_dict[vector.get_nodes()[i].get_id()].pos[1] = vector.get_nodes()[i].y
            
        qgv.save("./gv/" + vector_name + ".gv")
        
        self.layout_u.addWidget(qgv)
        self.qgv = qgv
        
    def save_node_positions(self, vector):
        i = 0
        if len(vector.get_nodes()) > 0:
            for node in self.qgv.engine.graph.nodes:
                try:
                    if not vector.get_nodes()[i].name == node.name:
                        i += 1
                    vector.get_nodes()[i].x = node.pos[0]
                    vector.get_nodes()[i].y = node.pos[1]
                    print("saving positions of node:", node.name)
                    i = i+1
                except:
                    print("index out of bounds")
                    return
        
    # Export GGraphViz widget into image
    def export(self, filename):
        try:
            self.qgv.grab().save(filename, "PNG")
            print("exported graph to: ", filename)
        except:
            print("Export of graph failed")

    # creates QGraphViz instance
    def create_QGraphViz(self):
        def node_selected(node):
            if(qgv.manipulation_mode==QGraphVizManipulationMode.Node_remove_Mode):
                print("Node {} removed".format(node))
            else:
                print("Node selected {}".format(node))
 
        def edge_selected(edge):
            if(qgv.manipulation_mode==QGraphVizManipulationMode.Edge_remove_Mode):
                print("Edge {} removed".format(edge))
            else:
                print("Edge selected {}".format(edge))
 
        def node_invoked(node):
            print("Node double clicked")
        def edge_invoked(node):
            print("Edge double clicked")
        def node_removed(node):
            print("Node removed")
        def edge_removed(node):
            print("Edge removed")
 
        show_subgraphs=True
        qgv= QGraphViz(
            show_subgraphs=show_subgraphs,
            auto_freeze= True, # show autofreeze capability
            node_selected_callback=node_selected,
            edge_selected_callback=edge_selected,
            node_invoked_callback=node_invoked,
            edge_invoked_callback=edge_invoked,
            node_removed_callback=node_removed,
            edge_removed_callback=edge_removed,
 
            hilight_Nodes=True,
            hilight_Edges=True
            )
 
        return qgv
       
    # Different functionalities for qgv that came with the library
    def manipulate():
        qgv.manipulation_mode=QGraphVizManipulationMode.Nodes_Move_Mode
 
    def save():
        fname = QFileDialog.getSaveFileName(qgv, "Save", "", "*.json")
        if(fname[0]!=""):
            qgv.saveAsJson(fname[0])
 
    def new():
        qgv.engine.graph = Graph("MainGraph")
        qgv.build()
        qgv.repaint()
 
    def add_node():
        dlg = QDialog()
        dlg.ok=False
        dlg.node_name=""
        dlg.node_label=""
        dlg.node_type="None"
        # Layouts
        main_layout = QVBoxLayout()
        l = QFormLayout()
        buttons_layout = QHBoxLayout()
 
        main_layout.addLayout(l)
        main_layout.addLayout(buttons_layout)
        dlg.setLayout(main_layout)
 
        leNodeName = QLineEdit()
        leNodeLabel = QLineEdit()
        cbxNodeType = QComboBox()
        leImagePath = QLineEdit()
 
        pbOK = QPushButton()
        pbCancel = QPushButton()
 
        cbxNodeType.addItems(["None","circle","box"])
        pbOK.setText("&OK")
        pbCancel.setText("&Cancel")
 
        l.setWidget(0, QFormLayout.LabelRole, QLabel("Node Name"))
        l.setWidget(0, QFormLayout.FieldRole, leNodeName)
        l.setWidget(1, QFormLayout.LabelRole, QLabel("Node Label"))
        l.setWidget(1, QFormLayout.FieldRole, leNodeLabel)
        l.setWidget(2, QFormLayout.LabelRole, QLabel("Node Type"))
        l.setWidget(2, QFormLayout.FieldRole, cbxNodeType)
        l.setWidget(3, QFormLayout.LabelRole, QLabel("Node Image"))
        l.setWidget(3, QFormLayout.FieldRole, leImagePath)
 
        def ok():
            dlg.OK=True
            dlg.node_name = leNodeName.text()
            dlg.node_label = leNodeLabel.text()
            if(leImagePath.text()):
                dlg.node_type = leImagePath.text()
            else:
                dlg.node_type = cbxNodeType.currentText()
            dlg.close()
 
        def cancel():
            dlg.OK=False
            dlg.close()
 
        pbOK.clicked.connect(ok)
        pbCancel.clicked.connect(cancel)
 
        buttons_layout.addWidget(pbOK)
        buttons_layout.addWidget(pbCancel)
        dlg.exec_()
 
        #node_name, okPressed = QInputDialog.getText(wi, "Node name","Node name:", QLineEdit.Normal, "")
        if dlg.OK and dlg.node_name != '':
                qgv.addNode(qgv.engine.graph, dlg.node_name, label=dlg.node_label, shape=dlg.node_type)
                qgv.build()
 
    def rem_node():
        qgv.manipulation_mode=QGraphVizManipulationMode.Node_remove_Mode
        for btn in buttons_list:
            btn.setChecked(False)
        btnRemNode.setChecked(True)
 

    def rem_edge():
        qgv.manipulation_mode=QGraphVizManipulationMode.Edge_remove_Mode
        for btn in buttons_list:
            btn.setChecked(False)
        btnRemEdge.setChecked(True)
 
    def add_edge():
        qgv.manipulation_mode=QGraphVizManipulationMode.Edges_Connect_Mode
        for btn in buttons_list:
            btn.setChecked(False)
        btnAddEdge.setChecked(True)
 
    
 
