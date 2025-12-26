
class Message:
    """A class to represent a message in the IM protocol.

    | header | payload | : 

    | header | : msg_id(1 byte) | timestamp(8 bytes, unix time) | length(int type, 4 bytes) |

    | payload | : The first 1 byte is msg_type; data, encoded in bytes,'length' field in header is determined by the length of payload.
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
