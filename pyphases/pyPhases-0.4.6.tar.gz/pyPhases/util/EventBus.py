from ..util.Logger import classLogger


class MissingOption(Exception):
    pass


class EventBus:
    eventMap = {}

    def on(self, eventName, function):

        if eventName not in self.eventMap:
            self.eventMap[eventName] = []
        self.eventMap[eventName].append(function)

    def trigger(self, eventName):
        if eventName not in self.eventMap:
            return
        for f in self.eventMap[eventName]:
            f()
