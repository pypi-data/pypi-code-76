import graphyte


class Client:

    def __init__(self, url='graphite', interval=60, prefix=None):
        self.graphite = graphyte.init(url, prefix=prefix, interval=interval)

    def send(self, stats, value=None, tags=None):
        self.graphite.send(stats, value=value, tags=tags)
