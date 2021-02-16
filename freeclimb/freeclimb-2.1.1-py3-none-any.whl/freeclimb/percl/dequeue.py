class Dequeue(dict):

    __cmd = 'Dequeue'

    def __init__(self):
        super().__init__()
        self.__setitem__(Dequeue.__cmd, {})
