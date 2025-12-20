from socket import socket
class MyServer:
    def __init__(self,host,port):
        self.host = host
        self.port = port
    def start(self):
        # input("Server started on {}:{}. Press Enter to stop.".format(self.host,self.port))
        s = socket() # create a socket object
        s.bind((self.host,self.port))
        s.listen()
        client_info = s.accept()
        print("Connection from:",client_info[1])