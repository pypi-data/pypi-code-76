import socket
import struct
from time import sleep


class Connection:
    SERVER="127.0.0.1"
    PORT = 5038
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    LoggedIn = False
    def __init__(self, server: str, port: int, username: str, password: str):
        self.SERVER = server
        self.PORT = port
        self.s.connect((self.SERVER, self.PORT))
        #self.conn, self.addr = self.s.accept()

        data = self.s.recv(self.BUFFER_SIZE)
        if data.decode("utf-8").__contains__("Asterisk"):
            data = self.send("Action: login\r\nUsername: {0}\r\nSecret: {1}\r\n\r\n".format(username, password).encode("utf-8"))
            if data.__contains__("Success"):
                self.LoggedIn = True
            if data.__contains__("Error"):
                self.close()

    def send(self, message: bytes, timeout:int = .1):
        self.s.send(message)
        sleep(.1)
        data = self.recvall(self.s, timeout)
        return data

    def recvall(self, sock, timeout:int):
        # Helper function to recv n bytes or return None if EOF is hit
        recvdata = ""
        while(1):
            sleep(timeout)
            newdata = sock.recv(self.BUFFER_SIZE)
            recvdata = recvdata + newdata.decode("utf-8")
            if newdata[-4:].decode("utf-8") == "\r\n\r\n":
                break
        return recvdata

    def close(self):
        self.s.close()
