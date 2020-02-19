nodes = [[]]
class Vector:
    vector_name = ''
    nodes = [['0001','node1','1/1/20','node description here', 'node0100','2','white team','check mark', 'artifact','true'],
            ['0002','node2','1/1/20','node description here', 'node0103','2','blue team','blue dot', 'artifact','true'],
            ['0003','node3','1/5/20','node description here', 'node0102','2','red team','red dot', 'artifact','false'],
            ['0004','node4','1/8/20','node description here', 'node0103','2','blue team','blue dot', 'artifact','false'],
            ['0005','node5','1/10/20','node description here', 'node0104','2','white team','check mark', 'artifact','true']]


    def __init__ (self, size):
        vector_name = 'Vector' + size


    def append_node_to_vector(node):
        nodes.append(node)

    
    for i in nodes:
        for j in i:
            #print(j, end = " ") #For testing purposes
            append_node_to_vector(j) #Appends node and its attributes to vector


#id, name,date, descripton,reference,column,creator,iconType,artifact,visibility


class DemoData:
    vector_list = []

    def add_vector():
        new_vector = Vector(vector_list.size)
        vector_list.append(new_vector)

    







