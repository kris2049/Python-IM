from asyncio import wait
from socket import socket
import sys
import os
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from protocol.message import Message
from protocol.codec import Codec
from server.network.connection import Connection
class MyClient:
    def __init__(self, host, port,name):
        self.name = name
        self.host = host
        self.port = port
        self.buffer = b""

    def start(self):
        print(f"Client {self.name} connecting to server at {self.host}:{self.port}")
        s = socket()
        s.connect((self.host, self.port))
        s.setblocking(True)
        st = "Hello, Hans!"
        data = st.encode('utf-8')
        timestamp = time.time()
        length = len(data)

        header = Message.Header(1, timestamp, length)
        msg = Message(header, data)


        data = Codec.encode(msg)

        # time.sleep(20)

        s.send(data)

        conn = Connection(s, None)


        try:
            data = s.recv(4096)
            if data:
                message = Codec.decode(data)
                print("message decoded")
                print(f"Received message: {message.payload}")
            else:
                print("No data received, closing connection.")
        except Exception as e:
            print("receive data error:", e) 

        finally:
            s.close()
            print("Connection closed.")
