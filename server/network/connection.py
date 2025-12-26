from socket import socket
import selectors
import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from protocol.message import Message
from protocol.constants import HEADER_SIZE, MSG_ID_SIZE, TIMESTAMP_SIZE, LENGTH_SIZE, TIMESTAMP_IDX, PAYLOAD_LEN_IDX
from protocol.codec import Codec
class Connection:
    def __init__(self, sock: socket, selector: selectors.DefaultSelector):

        self.sock = sock
        self.buffer = b""                                             # Buffer to hold incoming data
        self.selector = selector
        # self.alive = True                                             # Connection status

    def _close(self):
        """Close the connection."""
        self.alive = False
        self.selector.unregister(self.sock)
        self.sock.close()                                          # Server will close the socket when needed

    def handle_connection(self):
        """Handle the connection lifecycle."""
        print("Handling connection...")
        try:
            data = self.receive_data()
            if data:
                for message in self.decode_data():
                    print("message decoded")
                    self.handle_message(message)
            else:
                self._close()
        except Exception as e:
            self._close()
            print("receive data error:", e)

    def receive_data(self):
        """Receive data from the socket and store it in the buffer."""
        print("receiving data...")
        try:
            data = self.sock.recv(4096)
            if data:
                self.buffer += data
            return data
        except Exception as e:
            print("Error receiving data:", e)
            return None

    def decode_data(self):
        """
            Decode 0 or more complete messages from buffer, return a Iterator of Message objects.
            Yield Message objects as they are decoded.
            This method is a generator.
        """
        print("decoding data...")

        while True:
            print("decoding loop...")
            if(len(self.buffer) < HEADER_SIZE):                       # The header is 13 bytes long       The size of buffer is less than header size
                print("buffer size less than header size")
                break
            payload_len = int.from_bytes(self.buffer[PAYLOAD_LEN_IDX:PAYLOAD_LEN_IDX+LENGTH_SIZE], byteorder='big')    # Extract payload length from header

            print("payload_len:",payload_len)

            if len(self.buffer) < HEADER_SIZE + payload_len:         # The size of buffer is less than a complete message
                print("buffer size less than complete message")
                break
        
            msg_id = self.buffer[0].to_bytes(1,byteorder='big')                         # 1 byte
            timestamp = self.buffer[TIMESTAMP_IDX:TIMESTAMP_IDX+TIMESTAMP_SIZE]
            length = payload_len.to_bytes(4,byteorder='big')                            
            payload = self.buffer[HEADER_SIZE:HEADER_SIZE + payload_len]     # variable length

            data = msg_id+timestamp+length+payload



            message = Codec.decode(data)
            # print(f"Received message ID: {message.msg_id}, Timestamp: {message.timestamp}, Length: {message.length}, Payload: {message.payload}")
            # Remove the processed message from the buffer
            self.buffer = self.buffer[HEADER_SIZE + payload_len:]
            yield message




    def handle_message(self,message: Message):
        """Process the decoded message."""
        print(f"Received message ID: {message.header.msg_id}, Timestamp: {message.header.timestamp}, Length: {message.header.length}, Payload: {message.payload}")
        
