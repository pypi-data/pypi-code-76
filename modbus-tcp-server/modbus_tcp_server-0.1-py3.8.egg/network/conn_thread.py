from satella.coding import silence_excs
from satella.coding.concurrent import TerminableThread
import socket
import logging

from modbus_tcp_server.datagrams import MODBUSTCPMessage

logger = logging.getLogger(__name__)


class ConnectionThread(TerminableThread):
    def __init__(self, sock, addr, server):
        super().__init__(terminate_on=socket.error, daemon=True)
        self.socket = sock
        self.server = server
        self.addr = addr
        self.socket.setblocking(True)
        self.socket.settimeout(5)
        self.buffer = bytearray()

    def cleanup(self):
        self.socket.close()

    @silence_excs(socket.timeout)
    def loop(self):
        if self.server._terminating:
            self.terminate()
            return
        data = self.socket.recv(256)
        if not data:
            raise socket.error()
        logger.info('Received %s', repr(data))
        self.buffer.extend(data)

        # Extract MODBUS packets
        while self.buffer:
            try:
                packet = MODBUSTCPMessage.from_bytes(self.buffer)
                del self.buffer[:len(packet)]
            except ValueError:
                break

            msg = self.server.process_message(packet)
            b = bytes(msg)
            logger.debug('Sent %s', repr(b))
            self.socket.sendall(b)
