class Pause(dict):

    __cmd = 'Pause'

    def __init__(self, length):
        super().__init__()
        self.__setitem__(Pause.__cmd, {})
        self.length(length)

    def length(self, length):
        self.__getitem__(Pause.__cmd)['length'] = length
        return self
