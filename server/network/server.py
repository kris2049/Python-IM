import selectors
from socket import socket
class MyServer:
    def __init__(self,host,port):
        self.host = host
        self.port = port
    def start(self):
                                                                # input("Server started on {}:{}. Press Enter to stop.".format(self.host,self.port))
        s = socket()                                            # create a socket object
        s.bind((self.host,self.port))                           # bind to the port. Only registery, not listening yet
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
            for key,_ in s2:
                if key.data["type"] == "listener":                                                          # New connection event
                    client_info = key.fileobj.accept()                                                      # accept the new connection
                    print("Connection from:",client_info[1])
                    selector.register(client_info[0], selectors.EVENT_READ, data={"type": "client"})        # register the new client socket to selector to monitor read events
                elif key.data["type"] == "client":                        # Data from existing client
                    try:
                        data = key.fileobj.recv(1024)                         # receive data or close from the client
                    except Exception as e:
                        print("Error receiving data:", e)
                        data = None
                    if not data:                                          # if data is empty, the client has closed the connection
                        selector.unregister(key.fileobj)                  # unregister the socket from selector
                        key.fileobj.close()                               # close the socket
                        print("Client disconnected")
                    else:
                        print("Received data from client:", data)
