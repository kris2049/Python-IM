import struct
from protocol.message import Message
from protocol.constants import HEADER_SIZE, MSG_ID_SIZE, TIMESTAMP_SIZE, LENGTH_SIZE, TIMESTAMP_IDX, PAYLOAD_LEN_IDX
class Codec:
    """
        A class to represent the codec for encoding and decoding messages.

        | header | payload | : 

        | header | : msg_id(1 byte) | timestamp(8 bytes, unix time) | length(int type, 4 bytes) |

        | payload | : The first 1 byte is msg_type; data, encoded in bytes,'length' field in header is determined by the length of payload.
    """
    @staticmethod
    def encode(message: Message) -> bytes:
        """Encode a Message object into bytes."""
        header = bytearray()
        header += message.header.msg_id.to_bytes(MSG_ID_SIZE,'big')
        header += struct.pack('>d', message.header.timestamp)  # 浮点数用 struct.pack
        header += message.header.length.to_bytes(LENGTH_SIZE,'big')
        payload = message.payload
        return bytes(header) + payload

    @staticmethod
    def decode(data: bytes) -> Message:
        """
        Decode bytes into a Message object.
        | header | : msg_id(1 byte) | timestamp(8 bytes, unix time) | length(int type, 4 bytes) |
        """
        msg_id = data[0]
        timestamp = struct.unpack('>d', data[1:9])[0]
        length = int.from_bytes(data[9:13],byteorder='big')
        payload = data[13:13+length]
        header = Message.Header(msg_id, timestamp, length)
        return Message(header, payload)

        