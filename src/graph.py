from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QPushButton, QInputDialog, QLineEdit, QLabel
from QGraphViz.QGraphViz import QGraphViz, QGraphVizManipulationMode
from QGraphViz.DotParser import Graph, GraphType
from QGraphViz.Engines import Dot

 
class graph(QWidget): 
    
    qgv = ""
    
    def __init__(self, layout, vector=None):
        self.vector = vector
        self.qgv = self.create_QGraphViz()
        self.layout_u = layout
        self.read_vector_table(vector)
 
    def set_vector(self, vector):
        if not self.vector == vector:
            self.vector = vector
        self.qgv = self.create_QGraphViz()
        print("refresh")
        self.update_graph(vector)
    
        
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
            qgv.save("test.gv")
 
            # Add the QGraphViz object to the layout
            self.layout_u.addWidget(qgv)
            self.qgv = qgv
        else:
            self.update_graph(vector)
        
        
    def update_graph(self,vector):
        show_subgraphs=True
        
        qgv =self.qgv
        show_subgraphs=True
        qgv.setStyleSheet("background-color:white;")
        # Create A new Graph using Dot layout engine
        qgv.new(Dot(Graph("Main_Graph"), show_subgraphs=show_subgraphs))

        vector_name = vector.name
        
        
        if((self.layout_u.count())>0):
                while self.layout_u.count():
                    child = self.layout_u.takeAt(0)
                    if child.widget() :
                        child.widget().deleteLater()
                        
        
        for i in range(len(vector.get_nodes())):
            node_name = (vector.get_nodes()[i].get_name())
            node_type = (vector.get_nodes()[i].get_log_creator())
            
            print(node_type)
            
            if node_type == 'red' or node_type =='blue' or node_type == "white":
                print(type(node_type))
                color = node_type
                
            else:
                print(node_type + "not grey")
                color = "grey"
                
            
            print("adding node")
            n = self.qgv.addNode(qgv.engine.graph, node_name, label=node_name, fillcolor=color)
            
        qgv.build()
            
        qgv.save(vector_name + ".gv")
        
        self.layout_u.addWidget(qgv)
        qgv = qgv
        
 
           
 
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
 
    def load():
        fname = QFileDialog.getOpenFileName(qgv, "Open", "", "*.json")
        if(fname[0]!=""):
            qgv.loadAJson(fname[0])
 
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
 
    def add_subgraph():
        dlg = QDialog()
        dlg.ok=False
        dlg.subgraph_name=""
        dlg.subgraph_label=""
        dlg.subgraph_type="None"
        # Layouts
        main_layout = QVBoxLayout()
        l = QFormLayout()
        buttons_layout = QHBoxLayout()
 
        main_layout.addLayout(l)
        main_layout.addLayout(buttons_layout)
        dlg.setLayout(main_layout)
 
        leSubgraphName = QLineEdit()
        leSubgraphLabel = QLineEdit()
 
        pbOK = QPushButton()
        pbCancel = QPushButton()
 
        pbOK.setText("&OK")
        pbCancel.setText("&Cancel")
 
        l.setWidget(0, QFormLayout.LabelRole, QLabel("Subgraph Name"))
        l.setWidget(0, QFormLayout.FieldRole, leSubgraphName)
        l.setWidget(1, QFormLayout.LabelRole, QLabel("Subgraph Label"))
        l.setWidget(1, QFormLayout.FieldRole, leSubgraphLabel)
 
        def ok():
            dlg.OK=True
            dlg.subgraph_name = leSubgraphName.text()
            dlg.subgraph_label = leSubgraphLabel.text()
            dlg.close()
 
        def cancel():
            dlg.OK=False
            dlg.close()
 
        pbOK.clicked.connect(ok)
        pbCancel.clicked.connect(cancel)
 
        buttons_layout.addWidget(pbOK)
        buttons_layout.addWidget(pbCancel)
        dlg.exec_()
 
        if dlg.OK and dlg.subgraph_name != '':
                qgv.addSubgraph(qgv.engine.graph, dlg.subgraph_name, subgraph_type= GraphType.SimpleGraph, label=dlg.subgraph_label)
                qgv.build()
 
    def rem_subgraph():
        qgv.manipulation_mode=QGraphVizManipulationMode.Subgraph_remove_Mode
        for btn in buttons_list:
            btn.setChecked(False)
        btnRemSubGraph.setChecked(True)
