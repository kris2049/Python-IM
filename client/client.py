import socket
import sys
import os
import time
import threading # 1. 引入线程模块
import struct

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from common.protocol.message import Message
from common.protocol.codec import Codec
from common.protocol.constants import MSG_TYPE_LOGIN, MSG_TYPE_CHAT, HEADER_SIZE, PAYLOAD_LEN_IDX, LENGTH_SIZE

class MyClient:
    def __init__(self, host, port, name):
        self.name = name
        self.host = host
        self.port = port
        self.sock = socket.socket() # 创建 socket
        self.running = True         # 控制线程退出的标志

    def start(self):
        print(f"Client {self.name} connecting to server at {self.host}:{self.port}")
        try:
            self.sock.connect((self.host, self.port))
        except Exception as e:
            print(f"Failed to connect: {e}")
            return

        # --- 1. 先发送登录消息 ---
        self.send_login()

        # --- 2. 启动接收线程 (耳朵) ---
        # target 指向我们要在这个线程里运行的函数
        recv_thread = threading.Thread(target=self.receive_loop)
        recv_thread.daemon = True # 设置为守护线程，主程序退出时它也会自动退出
        recv_thread.start()

        # --- 3. 主线程负责输入发送 (嘴巴) ---
        self.input_loop()

    def send_login(self):
        """发送登录包"""
        print("Sending login info...")
        data = self.name.encode('utf-8')
        timestamp = time.time()
        length = len(data)
        
        # 使用 MSG_TYPE_LOGIN (假设在 constants 里定义为 1)
        header = Message.Header(MSG_TYPE_LOGIN, timestamp, length)
        msg = Message(header, data)
        packet = Codec.encode(msg)
        self.sock.send(packet)

    def receive_loop(self):
        """
        这个函数会在后台线程一直在运行。
        它负责不断地收数据，处理粘包，然后打印。
        """
        buffer = b""
        while self.running:
            try:
                # 阻塞接收，但因为在独立线程，不会影响你输入
                chunk = self.sock.recv(4096)
                if not chunk:
                    print("\nServer closed connection.")
                    self.running = False
                    break
                
                buffer += chunk
                
                # --- 处理粘包/解包逻辑 (复用你之前的逻辑) ---
                while True:
                    if len(buffer) < HEADER_SIZE:
                        break # 数据不够头部，继续收
                    
                    # 解析 payload 长度
                    payload_len = int.from_bytes(buffer[PAYLOAD_LEN_IDX:PAYLOAD_LEN_IDX+LENGTH_SIZE], byteorder='big')
                    
                    if len(buffer) < HEADER_SIZE + payload_len:
                        break # 数据不够完整包，继续收
                    
                    # 截取完整的一条消息
                    packet_data = buffer[:HEADER_SIZE + payload_len]
                    buffer = buffer[HEADER_SIZE + payload_len:] # 剩下的放回缓冲
                    
                    # 解码并显示
                    msg = Codec.decode(packet_data)
                    self.handle_message(msg)

            except Exception as e:
                print(f"\nReceive error: {e}")
                self.running = False
                break

    def handle_message(self, message: Message):
        """处理收到的消息"""
        # \r 是为了清除当前的输入提示符，让输出好看点
        content = message.payload.decode('utf-8')
        print(f"\n[Server/Chat]: {content}")
        # 重新打印输入提示符
        print("Say something: ", end="", flush=True)

    def input_loop(self):
        """主线程循环等待输入"""
        # 稍微等一下让登录消息发完
        time.sleep(0.5) 
        
        while self.running:
            try:
                text = input("Say something: ")
                if text == 'exit':
                    self.running = False
                    break
                
                # 发送聊天消息 MSG_TYPE_CHAT (假设为 2)
                data = text.encode('utf-8')
                timestamp = time.time()
                length = len(data)
                
                header = Message.Header(MSG_TYPE_CHAT, timestamp, length)
                msg = Message(header, data)
                packet = Codec.encode(msg)
                
                self.sock.send(packet)
                
            except Exception as e:
                print(f"Send error: {e}")
                break
        
        self.sock.close()
        print("Client exited.")

if __name__ == "__main__":
    # 为了测试，你可以把名字换成 input 获取
    name = input("Enter your name: ")
    client = MyClient("127.0.0.1", 9000, name)
    client.start()