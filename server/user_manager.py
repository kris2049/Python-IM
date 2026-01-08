from common.network.connection import Connection
from common.protocol.message import Message
class UserManager:
    def __init__(self):
        # A dictionary to hold user information
        # Key: username(str), Value: conn(Connection)
        self.users = []

    def add_user(self,conn: Connection):
        """Add a new user to the manager."""
        if conn in self.users:
            print(f"User {conn.sock} already exists.")
        else:
            self.users.append(conn)
            print(f"User {conn.sock} added.")

    def remove_user(self, conn: Connection):
        """Remove a user from the manager."""
        if conn in self.users:
            self.users.remove(conn)
            print(f"User {conn.sock} removed.")
        else:
            print(f"User {conn.sock} not found.")

    def get_connection(self, conn: Connection):
        """Get the connection object for a given user."""
        if conn in self.users:
            return conn
        return None

    def brodcast_message(self, message: Message, sender_conn: Connection):
        """Broadcast a message to all connected users. Except the sender."""
        for conn in self.users:
            if conn == sender_conn:
                continue
            conn.send_message(message)
            print(f"Broadcasted message to {conn.sock}.")

    def list_users(self):
        """List all connected users."""
        return [conn.sock for conn in self.users]

    
    

    
