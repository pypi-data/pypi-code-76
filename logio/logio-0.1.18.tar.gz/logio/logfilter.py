


LOG_FILTER_TYPES = {}

def register_filter_type(name, klass):
    LOG_FILTER_TYPES[name] = klass

def unregister_filter_type(name):
    del LOG_FILTER_TYPES[name]

def get_filter_class(name):
    return LOG_FILTER_TYPES.get(name, None)
    
class LogFilter(object):

    def __init__(self, settings):
        self.settings = settings or {}

    def line_filter(self, line):
        raise NotImplementedError()

    @classmethod
    def init(cls, settings):
        filter_type = settings.get("type", "icontains")
        filter_class = get_filter_class(filter_type)
        if not filter_class:
            return None
        return filter_class(settings)


class ContainsFilter(LogFilter):

    def line_filter(self, line):
        substrings = self.settings.get("substrings", [])
        for substring in substrings:
            if not substring in line:
                return False
        return True

class IContainsFilter(LogFilter):

    def line_filter(self, line):
        line = line.lower()
        substrings = self.settings.get("substrings", [])
        for substring in substrings:
            if not substring.lower() in line:
                return False
        return True

register_filter_type("contains", ContainsFilter)
register_filter_type("icontains", IContainsFilter)
