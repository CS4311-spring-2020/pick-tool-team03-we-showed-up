from random import randint
import csv


class Vector:
    vector_checked = True
    vector_name = ''
    vector_description = ''
    nodes = []
    relationships = []

    def __init__ (self, size):
        self.vector_name = 'Vector' + (str(size))

    def append_node(self, node):
        self.nodes.append(node.copy())

    def append_relationship(self, relationship):
        self.relationships.append(relationship.copy())


class DemoData:
    vector1 = Vector(1)
    vector_list = [vector1]

    # id, name,date, description, reference, column, creator, iconType, artifact, visibility
    vector_list[0].nodes = [[str(randint(0,9999)),'node1','1/1/20','node description here', 'node0100','white team','white team','check mark', 'artifact',True],
                            [str(randint(0,9999)),'node2','1/1/20','node description here', 'node0103','white team','blue team','blue dot', 'artifact', True],
                            [str(randint(0,9999)),'node3','1/5/20','node description here', 'node0102','white team','red team','red dot', 'artifact', False],
                            [str(randint(0,9999)),'node4','1/8/20','node description here', 'node0103','white team','blue team','blue dot', 'artifact', False],
                            [str(randint(0,9999)),'node5','1/10/20','node description here', 'node0104','white team','white team','check mark', 'artifact', True]]

    vector_list[0].relationships = [[str(randint(0,999)), 'Relationship1', '0001', '0002'],
                                    [str(randint(0,999)), 'Relationship2', '0001', '0003'],
                                    [str(randint(0,999)), 'Relationship3', '0002', '0004']]

    vector_list[0].vector_description = "Description of vector 1"

    def add_vector(self):
        new_vector = Vector(len(self.vector_list)+1)
        self.vector_list.append(new_vector)

