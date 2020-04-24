# This Python file uses the following encoding: utf-8
import threading
import socket

class Network:
    def __init__(self):
        # Ask clients what port they would like to connect through
        self.port = 8091
        #local port for now
        #lead_ip = '127.0.0.1'
        # Lead socket
        self.socket = socket.socket()

        self.serverStatus = False

        pass

    def start_lead_server(self):
        s = socket.socket()
        print ("Socket successfully created")
        s.bind(('', self.port))
        print ("socket binded to %s" %(self.port))

        self.socket = s
        self.serverStatus == True

        #20 connections will be accepted per SRS
        self.socket.listen(20)
        print ("socket is listening")
        thread = threading.Thread(target=self.start_server_thread)
        thread.start()

    def start_server_thread(self):
        while (self.serverStatus == True):
            print('Hi')
            # Establish connection with client.
            c, addr = self.socket.accept()
            print ('Got connection from', addr)

            # send a thank you message to the client.
            c.send('Thank you for connecting')

            # Close the connection with the client
            # c.close()

    def close_server(self):
        self.socket.close()
        self.serverStatus = False
        self.socket = socket.socket()

    def connect_analyst_to_lead(self, lead_ip):
        s = socket.socket()

        # Define the port on which you want to connect

        # connect to the server on local computer
        s.connect((lead_ip, self.port))

        # receive data from the server
        print (s.recv(1024))
        print("here?")
        # close the connection
        # s.close()
