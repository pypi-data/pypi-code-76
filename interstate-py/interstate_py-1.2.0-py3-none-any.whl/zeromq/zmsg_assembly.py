import io
from typing import List

from interstate_py.interstate_message import InterstateMessageAssembly, InterstateWireMessage
from interstate_py.internalio.data_output_stream import DataOutputStream
from interstate_py.internalio.data_input_stream import DataInputStream


class ZMsgAssembly(InterstateMessageAssembly):
    """
    Serializes / Deserializes a InterstateMessage from the given ZMQMessage
    """
    @staticmethod
    def assemble(msg: InterstateWireMessage) -> List[bytes]:
        stream = io.BytesIO()
        dos = DataOutputStream(stream)
        try:
            dos.write_int(len(msg.header))
            for k, v in msg.header.items():
                dos.write_utf("{}:{}".format(k, v))
                dos.write_bytes(bytes([0x00]))
            dos.write_bytes(msg.payload)
            return [msg.identity, dos.to_bytes()]
        finally:
            dos.close()

    @staticmethod
    def disassemble(msg: List[bytes]) -> InterstateWireMessage:
        identity = msg[0]
        stream = io.BytesIO(msg[1])
        dis = DataInputStream(stream)
        header_length = dis.read_int()

        header = {}
        for _ in range(0, header_length):
            k, v = dis.read_utf().split(':')
            dis.read_byte()
            header[k] = v
        payload = dis.read_bytes()
        stream.close()
        return InterstateWireMessage(identity, header, payload)
