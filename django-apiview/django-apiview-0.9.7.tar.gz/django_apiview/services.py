
""" not ready...

class Service(object):
    
    def __call__(self, *args, **kwargs):
        return self.main(*args, **kwargs)

    @classmethod
    def serve(cls, *args, **kwargs):
        return cls()(*args, **kwargs)


class PingService(Service):

    def main(self):
        return "pong"

class EchoService(Service):

    def main(self, msg):
        return msg


 
@apiview
@cache("test:ping")
def ping():
    return PingService.serve()

@apiview
@cache("test:echo", related_services=[PingService])
def echo(msg):
    return PingService.serve(msg)

"""