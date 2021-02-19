from .device import Device
from .config_store import Config
from .exec_protocol import ExecProtocol

import os, socket, ssl, json, time, logging

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


class PasswordError(Exception):
    pass

class NetDevice(Device):

    def __init__(self, url):
        super().__init__(url)

    def read(self, size=None):
        r,_,_ = select.select([self.__socket], [], [], 0.1)
        if size == None: size = 1024
        return self.__socket.recv(size) if r else b''

    def write(self, data):
        self.__socket.sendall(data)

    def __enter__(self):
        self.__connect()
        return ExecProtocol(self)

    def __exit__(self, typ, value, traceback):
        self.write(b'bye\n')
        # make sure all data is sent???
        # time.sleep(0.2)
        self.__socket.close()
        self.__socket = None

    def __connect(self):
        # establish connection to server
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = self.address.split(':')
        # don't wait long for the connection
        self.__socket.settimeout(1)
        self.__socket.connect((host, int(port)))
        self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # password check
        msg = { 'password': Config.get_secret('password', '???') }
        msg = json.dumps(msg).encode()
        self.write(msg)
        self.write(b'\n')
        msg = self.read_all()
        if msg != b'ok':
            raise PasswordError(msg)
