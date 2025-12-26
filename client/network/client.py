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
class MyClient:
    def __init__(self, host, port,name):
        self.name = name
        self.host = host
        self.port = port

    def start(self):
        print(f"Client {self.name} connecting to server at {self.host}:{self.port}")
        s = socket()
        s.connect((self.host, self.port))
        st = "Hello, Hnery!"
        data = st.encode('utf-8')
        timestamp = int(time.time()).to_bytes(8,byteorder='big')
        length = len(data).to_bytes(4,byteorder='big')

        header = Message.Header(1, timestamp, length)
        msg = Message(header, data)


        data = Codec.encode(msg)

        data2 = b"1"

        time.sleep(10)

        s.send(data)

        

        # s.close()
