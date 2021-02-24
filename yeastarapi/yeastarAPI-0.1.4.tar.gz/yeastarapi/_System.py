import socket


def PortStatus(conn, port: int):
    return conn.send("Action: SMSCommand\r\ncommand: gsm show {0}\r\n\r\n".format(port+1).encode("utf-8"))
