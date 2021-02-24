import io
import struct


class DataInputStream:
    """
    Reads binary data from a BytesIO stream - similar to a java DataInputStream
    :info internal use only
    """

    def __init__(self, stream: io.BytesIO):
        self.stream = stream

    def read_byte(self):
        return struct.unpack('b', self.stream.read(1))[0]

    def read_int(self) -> int:
        return struct.unpack('>i', self.stream.read(4))[0]

    def read_utf(self) -> str:
        utf_length = struct.unpack('>h', self.stream.read(2))[0]
        return self.stream.read(utf_length).decode("utf-8")

    def read_bytes(self) -> bytes:
        """
        :return: remaining bytes from the stream
        """
        return self.stream.read()

    def close(self):
        return self.stream.close()
