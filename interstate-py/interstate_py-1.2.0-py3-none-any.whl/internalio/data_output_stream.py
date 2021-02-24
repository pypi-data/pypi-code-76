import io
import struct


class DataOutputStream:
    """
    Writes data to a BytesIO stream - similar to a java DataOutputStream
    :info internal use only
    """
    def __init__(self, stream: io.BytesIO):
        self.stream = stream

    def write_bytes(self, b: bytes) -> int:
        return self.stream.write(b)

    def write_int(self, i: int) -> int:
        return self.stream.write(int.to_bytes(i, 4, 'big'))

    def write_utf(self, s: str) -> int:
        self.stream.write(struct.pack('>h', len(s)))
        return self.stream.write(s.encode("utf-8"))

    def to_bytes(self) -> bytes:
        return self.stream.getvalue()

    def close(self):
        return self.stream.close()