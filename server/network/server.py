import selectors
from socket import socket
from network.connection import Connection
class MyServer:
    def __init__(self,host,port):
        self.host = host
        self.port = port
    def start(self):
                                                                # input("Server started on {}:{}. Press Enter to stop.".format(self.host,self.port))
        s = socket()                                            # create a socket object
        s.bind((self.host,self.port))                           # bind to the port. Only registery, not listening yet
        s.setblocking(False)
        s.listen()                                              # Tell the kenel we are ready to accept connections. listen() doesn't block
        #                                                       # Kernel will maintain two queues: 
        #                                                       # 1. incomplete connections(The SYN package from client and TCP connections during 3 times hand shake) 
        #                                                       # 2. completed connections(After 3 times hand shake, waiting for server to accept)
        # while True:        # wait for connections from clients
        #     client_info = s.accept()                          # accept a connection from completed connections queue. It only establishes the connection, doesn't care about data.
        #                                                       # accept() returns a socket object for the connection, and the address of the client.
        #     print("Connection from:",client_info[1])
        selector = selectors.DefaultSelector() 

        selector.register(s,selectors.EVENT_READ,data={"type": "listener"})                                 # register the new socket to selector to monitor read events



        while True:                        
            s2 = selector.select()                                                                          # This will block until there is an event on the socket
            for key,event_mask in s2:
                if event_mask & selectors.EVENT_READ:
                    if key.data["type"] == "listener":                                                          # New connection event
                        client_info = s.accept()                                                      # accept the new client connection
                        print("Connection from:",client_info[1])
                        client_info[0].setblocking(False)
                        conn = Connection(client_info[0],selector)                                              # create a Connection object to handle this client
                        selector.register(client_info[0], selectors.EVENT_READ, data={"type":"client", "conn": conn})   # register the new client socket to selector with Connection object 
                    elif key.data["type"] == "client":                        # Data from existing client
                        conn = key.data["conn"]
                        try:
                            conn.handle_connection(event_mask)                                      # handle the connection
                        except Exception as e:
                            print("Error handling connection:", e)
                elif event_mask & selectors.EVENT_WRITE:
                    conn = key.data["conn"]
                    try:
                        conn.handle_connection(event_mask)
                    except Exception as e:
                        print("Error handling connection:",e)
