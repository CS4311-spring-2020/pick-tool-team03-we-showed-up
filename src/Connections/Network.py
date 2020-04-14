# This Python file uses the following encoding: utf-8
import socket

class Network:
    def __init__(self):
        # Ask clients what port they would like to connect through
        port = 12345
        #local port for now
        lead_ip = '127.0.0.1'
        pass

    def start_lead_server(self):
        s = socket.socket()
        print ("Socket successfully created")
        s.bind(('', port))
        print ("socket binded to %s" %(port))

        #20 connections will be accepted per SRS
        s.listen(20)
        print ("socket is listening")

        while True:

           # Establish connection with client.
           c, addr = s.accept()
           print ('Got connection from', addr)

           # send a thank you message to the client.
           c.send('Thank you for connecting')

           # Close the connection with the client
           c.close()

    def connect_analyst_to_lead(self):
        s = socket.socket()

        # Define the port on which you want to connect

        # connect to the server on local computer
        s.connect((lead_ip, port))

        # receive data from the server
        print (s.recv(1024))
        # close the connection
        s.close()
