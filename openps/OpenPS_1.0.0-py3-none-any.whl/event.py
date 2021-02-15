import os

class Event:

    def __init__(self, plugins_path):
        self.path = plugins_path
        self.events = {}

    def init(self):
        lst = os.listdir(self.path)
        if "__init__.py" in lst:
            lst.remove("__init__.py")
        for file in lst:
            file = os.path.abspath(self.path + file)
            if os.path.isfile(file):
                exec(open(file, "r").read())

    def create(self, name):
        self.events.update({name: []})

    def register(self, name):

        def inner(func):
            self.events[name].append(func)
            return func
        return inner

    def call(self, name):
        try:
            event = self.events[name]
        except:
            raise Exception("Unknown event. " + name)

        for func in event:
            func()
