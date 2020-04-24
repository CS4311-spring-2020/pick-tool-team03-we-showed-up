from maltego_trx.entities import Phrase

from maltego_trx.transform import DiscoverableTransform


class csv_data(DiscoverableTransform):
    """
    Returns a phrase greeting a person on the graph.
    """
    id_list = ["7417", "3217","1798","3512","588"]
    ##
    @classmethod
    def create_entities(cls, request, response):
        id = request.Value
        try:
            names = cls.get_name(id)
            if names:
                for name in names:
                    response.addEntity(Node, name)

            else:
                response.addUIMessage("The ID specified could not be found.")

        except IOError:
            response.addUIMessage("Could not read CSV file.", messageType=UIM_PARTIAL)

    # response.addEntity(Phrase, "Node ID: " % node_id)


    ##This funtion analyzes the .csv file to find associated Node_ID in respect to selected nodes.
    @staticmethod
    def get_name(search_name):
        node_name = []
        with open ("test.csv") as f:
            for line in f.readlines():
                id, name, time_stamp, desc, reference, creator, event_T, icon_T, artifact, visibility = line.split(",",9) #9 commas per line
                if id.strip() == search_id.strip():
                    node_name.append(name.strip())
        return node_name
    
    def all_id(self, id_list):
        for i in range(id_list):
            create_entities( i)
