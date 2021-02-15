import os

class Event:

    def __init__(self, plugins_path):
        self.path = plugins_path
        self.events = {}
        self.events.update({"OnProgramStart": []})
        self.events.update({"OnProgramExit": []})
        self.events.update({"OnProgramInit": []})

    def init(self):
        """This function initialize all plugins.
        If you have custom events then you need to call this function last."""
        lst = os.listdir(self.path)
        if "__init__.py" in lst:
            lst.remove("__init__.py")
        for file in lst:
            file = os.path.abspath(self.path + file)
            if os.path.isfile(file):
                exec(open(file, "r").read())

    def create(self, name):
        """Create your own event."""
        self.events.update({name: []})

    def register(self, name):
        """This decorator useable to register functions."""

        def inner(func):
            self.events[name].append(func)
            return func
        return inner

    def call(self, name):
        """The call() function call registered functions."""
        try:
            event = self.events[name]
        except:
            raise Exception("Unknown event. " + name)

        for func in event:
            func()
