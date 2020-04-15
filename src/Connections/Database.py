#Connect event config (Team directories)
from EventConfiguration import EventConfiguration
#Connect vector table
from Vector import Vector
#Connect node table 

import pymongo
from pymongo import MongoClient

class Database:
    def __init__(self):
        #Connection 
        client = MongoClient('mongodb+srv://localhost:localhost@cluster0-kycow.mongodb.net/test?retryWrites=true&w=majority')
        pick_database = client['PICK-Tool-Vector-Database']
        #Vector
        vd = Vector();
		
        #Push vector to db (Right side of window)
        VectorDBUser.pushButtonclicked.connect(self.insert_vector(pick_database, vd))
        #Pull vector to db (Right side)
        VectorDBUser.vdbc_button_pull.clicked.connect(self.update_vector(pick_database, vd))

    # This method gets the database specified in OpenEvent
    # For this demo the network will be setup this way instead of automatically choosing the event that the lead is working on
    def retrieve_database():
        # https://api.mongodb.com/python/current/tutorial.html
        #mongodb+srv://localhost:<localhost>@cluster0-kycow.mongodb.net/test?retryWrites=true&w=majority
        return

    #Upload vectors to the database
    #NOTE: since there is no UI to upload log files and event config to db, they are being handled here
    def insert_vector(db, vd):
        #Collections
        #pick_vectors = pick_database.vectors
        pick_nodes = db.nodes
        #pick_log_files = pick_database.log_files
        #pick_event_config = pick_database.event_config

        #Nodes
        node = vd.get_nodes(vd)

        #insert node vectors in documents
        for i in node:
            node_id = node[i].id
            node_name = node[i].name
            node_timestamp = node[i].timestamp
            node_description = node[i].description
            node_log_entry_reference = node[i].log_entry_reference
            node_log_creator = node[i].log_creator
            node_event_type = node[i].event_type
            node_source = node[i].source
            node_icon_type = node[i].icon_type
            node_visibility = node[i].visibility
            node_icon = node[i].icon
            node_x = node[i].x
            node_y = node[i].y
	
            #Node document 
            node_doc = {
                id: node_id,
                name: node_name,
                timestamp: node_timestamp,
                description: node_description,
                log_entry_reference: node_log_entry_reference,
                log_creator: node_log,
                event_type: node_event_type,
                source: node_source,
                icon_type: node_icon_type,
                visibility: node_visibility,
                icon: node_icon,
                x: node_x,
                y: node_y
	
            }
			
            result_nodes = pick_nodes.insert_one(node_doc);
			
        #Array with vectors
        #arr_vectors = []
        #arr_logFiles = []
        #arr_eventConfig = []
		
        #populate arr_vectors with vectors from local storage
        #arr_vectors = DemoData().vector_list[0].nodes;

        #Use for loop to retrieve vector database

        #Save data in bson document and insert it into db


        #insert vector array into db
        #result_vectors = pick_vectors.insert_many(arr_vectors)
        #result_logFiles = pick_log_files.insert_many(arr_logFiles)
        #result_eventConfig = pick_event_config.insert_many(arr_eventConfig)

        #Display all vectors inserted in database
        for object_vector in result_nodes.inserted_nodes:
            print('Vector added. The vector Id is ' + str(object_vector))

        #Display all log files inserted in database
        #for object_logFile in result_logFiles.inserted_logFiles:
            #print('Vector added. The vector Id is ' + str(object_logFile))
			
        #Display all events inserted in database
        #for object_eventConfig in result_eventConfig.inserted_events:
            #print('Vector added. The vector Id is ' + str(object_eventConfig))


    #Update version of vectors (may not be needed for this demo)
    def update_vector(db, vd):
        #Collection
        pick_vectors = pick_database.vectors

        pick_vectors= pick_vectors.find()
        #for vector in vectors:
            #Update local vectors
            #vector_result = pick_vectors.update_one({:}, {:{:}})

    def delete_vector(db, vd):
        pick_vectors = pick_database.vectors