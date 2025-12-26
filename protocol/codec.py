from protocol.message import Message
from protocol.constants import HEADER_SIZE, MSG_ID_SIZE, TIMESTAMP_SIZE, LENGTH_SIZE, TIMESTAMP_IDX, PAYLOAD_LEN_IDX
class Codec:
    """A class to represent the codec for encoding and decoding messages."""
    @staticmethod
    def encode(message: Message) -> bytes:
        """Encode a Message object into bytes."""
        header = bytearray()
        header.append(message.header.msg_id)
        header += message.header.timestamp
        header += message.header.length
        payload = message.payload
        return bytes(header) + payload

    @staticmethod
    def decode(data: bytes) -> Message:
        """
        Decode bytes into a Message object.
        | header | : msg_id(1 byte) | timestamp(8 bytes, unix time) | length(int type, 4 bytes) |
        """
        msg_id = data[0]
        timestamp = int.from_bytes(data[1:9], byteorder='big')
        length = int.from_bytes(data[9:13],byteorder='big')
        payload = data[13:13+length]
        header = Message.Header(msg_id, timestamp, length)
        return Message(header, payload)

        