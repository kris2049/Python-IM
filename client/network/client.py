from socket import socket
class MyClient:
    def __init__(self, host, port,name):
        self.name = name
        self.host = host
        self.port = port

    def start(self):
        print(f"Client {self.name} connecting to server at {self.host}:{self.port}")
        s = socket()
        s.connect((self.host, self.port))
        s.send(b"Hello, Server!")
        s.close()
