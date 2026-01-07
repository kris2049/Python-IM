
class Message:
    """A class to represent a message in the IM protocol.
    """

    class Header:
        """A class to represent the header of a message."""
        def __init__(self, msg_id: int, timestamp: int, length: int):
            self.msg_id = msg_id
            self.timestamp = timestamp
            self.length = length
    def __init__(self, header: Header, payload: any):
        self.header = header
        self.payload = payload
