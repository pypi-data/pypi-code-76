import socket

class messageResponse:
    Response = None
    Privilege = None
    ID = None
    Smsc = None
    Status = None
    def __init__(self, reply:str):
        self.Parse(reply)

    def Parse(self, reply:str):
        lines = reply.split("\r\n")
        for l in lines:
            print(l)
            if l.__contains__(": "):
                key, val = l.split(": ",1)
                if key == "Response":
                    self.Response = val
                elif key == "Privilege":
                    self.Privilege = val
                elif key == "ID":
                    self.ID = val
                elif key == "Smsc":
                    self.Smsc = val
                elif key == "Status":
                    self.Status = val


class messageReceived:
    Response = None
    Privilege = None
    ID = None
    GsmSpan = None
    Sender = None
    RecvTime = None
    Index = None
    Total = None
    Smsc = None
    Content = None
    def __init__(self, reply:str):
        self.Parse(reply)

    def Parse(self, reply:str):
        lines = reply.split("\r\n")
        for l in lines:
            print(l)
            if l.__contains__(": "):
                key, val = l.split(": ",1)
                if key == "Response":
                    self.Response = val
                elif key == "Privilege":
                    self.Privilege = val
                elif key == "ID":
                    self.ID = val
                elif key == "GsmSpan":
                    self.GsmSpan = val
                elif key == "Sender":
                    self.Sender = val
                elif key == "RecvTime":
                    self.RecvTime = val
                elif key == "Index":
                    self.Index = val
                elif key == "Total":
                    self.Total = val
                elif key == "Smsc":
                    self.Smsc = val
                elif key == "Content":
                    self.Content = val


def SendSMS(conn, port: int, destination: str, content: str):
    return messageResponse(conn.send("Action: SMSCommand\r\ncommand: gsm send sms {0} {1} \"{2}\" $id\r\n\r\n".format(port+1, destination, content).encode("utf-8"), 3))

