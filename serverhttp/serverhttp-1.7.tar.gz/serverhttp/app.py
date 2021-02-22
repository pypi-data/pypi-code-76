class App(object):
    def __init__(self, name):
        self.name = name
        self.routes = {}
    def route(self, path, method):
        def decorator(func):
            m = {key:func for key in method}
            self.routes[path] = m
            return func
        return decorator
    def prepare_for_deploy(self, srv):
        srv.functions.update(self.routes)
        srv.name = self.name
Application = App

