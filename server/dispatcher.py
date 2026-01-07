from common.network.connection import Connection
from common.protocol.message import Message
from common.protocol.constants import MSG_TYPE_CHAT, MSG_TYPE_HEARTBEAT, MSG_TYPE_ACK, MSG_TYPE_LOGIN

class Dispatcher:
    def __init__(self):
        self.connections = []
        self.handlers = {
            MSG_TYPE_CHAT: self.handle_chat_message,
            MSG_TYPE_HEARTBEAT: self.handle_heartbeat,
            MSG_TYPE_ACK: self.handle_ack_message,
            MSG_TYPE_LOGIN: self.handle_login
        }
    
    def dispatch(self, conn: Connection, message: Message):
        handler = self.handlers.get(message.header.msg_id)
        if handler:
            handler(conn,message)
        else:
            print(f"No handler for message ID {message.header.msg_id}")

    def handle_login(self, conn: Connection, message: Message):
        print(f"Handling login message: {message.payload}")
        # TODO: Implement login logic here

    
    def handle_chat_message(self, conn: Connection, message: Message):
        print(f"Handling chat message: {message.payload}")
        # TODO: Implement chat message logic here

    def handle_heartbeat(self, conn: Connection, message: Message):
        print("Handling heartbeat message")
        # TODO: Implement heartbeat logic here

    def handle_ack_message(self, conn: Connection, message: Message):
        print(f"Handling ACK message: {message.payload}")
        # TODO: Implement ACK logic here
        
