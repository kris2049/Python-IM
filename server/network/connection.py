from socket import socket
import selectors
import sys
import os
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)
from protocol.message import Message
from protocol.constants import HEADER_SIZE, MSG_ID_SIZE, TIMESTAMP_SIZE, LENGTH_SIZE, TIMESTAMP_IDX, PAYLOAD_LEN_IDX
from protocol.codec import Codec
class Connection:
    def __init__(self, sock: socket, selector: selectors.DefaultSelector):

        self.sock = sock
        self.read_buffer = b""                                             # Buffer to hold incoming data
        self.selector = selector
        self.write_buffer = b""                                            # Buffer to hold sending data

        # self.alive = True                                             # Connection status

    def _close(self):
        """Close the connection."""
        self.alive = False
        self.selector.unregister(self.sock)
        self.sock.close()                                          # Server will close the socket when needed

    def handle_connection(self, event_mask):
        """Handle the connection lifecycle."""
        print("Handling connection...")
        if event_mask & selectors.EVENT_READ:
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
        if event_mask & selectors.EVENT_WRITE:
            try:
                if self.write_buffer:
                    send_size = self.sock.send(self.write_buffer)
                    self.write_buffer = self.write_buffer[send_size:]               # Remove the sent bytes from the buffer 
                    if not self.write_buffer:
                        # Sending complete, modify selector to read only
                        self.selector.modify(self.sock,selectors.EVENT_READ,data={"type":"client","conn":self})                              # If all data is sent, stop monitoring write events
                        print("All data sent, modified selector to read only.")
            except Exception as e:
                print("Server send message error:",e)
                self._close()





    def receive_data(self):
        """Receive data from the socket and store it in the buffer."""
        print("receiving data...")
        try:
            data = self.sock.recv(4096)
            if data:
                self.read_buffer += data
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
            if(len(self.read_buffer) < HEADER_SIZE):                       # The header is 13 bytes long       The size of buffer is less than header size
                print("buffer size less than header size")
                break
            payload_len = int.from_bytes(self.read_buffer[PAYLOAD_LEN_IDX:PAYLOAD_LEN_IDX+LENGTH_SIZE], byteorder='big')    # Extract payload length from header

            print("payload_len:",payload_len)

            if len(self.read_buffer) < HEADER_SIZE + payload_len:         # The size of buffer is less than a complete message
                print("buffer size less than complete message")
                break

            data = self.read_buffer[0:HEADER_SIZE+payload_len]



            message = Codec.decode(data)

            self.read_buffer = self.read_buffer[HEADER_SIZE + payload_len:]               # clean the buffer
            yield message




    def handle_message(self,message: Message):
        """Process the decoded message."""
        print(f"Received message ID: {message.header.msg_id}, Timestamp: {message.header.timestamp}, Length: {message.header.length}, Payload: {message.payload}")

        # Server sends messages to the client
        st = "Hello, client!"
        data = st.encode('utf-8')
        timestamp = time.time()
        length = len(data)

        header = Message.Header(1, timestamp, length)
        rpl_msg = Message(header, data)
        self.send_message(rpl_msg)



    def send_message(self,message: Message):
        data = Codec.encode(message)
        self.write_buffer += data
        self.selector.modify(self.sock,selectors.EVENT_WRITE | selectors.EVENT_READ,data={"type":"client","conn":self})             # Modify selector to monitor write events
        
        send_size = self.sock.send(self.write_buffer)                   # send() will return the number of bytes sent
        self.write_buffer = self.write_buffer[send_size:]               # Remove the sent bytes from the buffer

        if not self.write_buffer:
            self.selector.modify(self.sock,selectors.EVENT_READ,data={"type":"client","conn":self})                              # If all data is sent, stop monitoring write events
            print("All data sent, modified selector to read only.")


        
        
