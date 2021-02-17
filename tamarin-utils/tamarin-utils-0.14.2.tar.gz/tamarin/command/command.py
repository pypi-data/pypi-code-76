class Command(object):
    def __init__(self, obj=None) -> None:
        self._obj = obj

    def execute(self):
        raise NotImplementedError
