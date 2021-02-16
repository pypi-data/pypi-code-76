class Reject(dict):

    __cmd = 'Reject'

    def __init__(self):
        super().__init__()
        self.__setitem__(Reject.__cmd, {})

    def reason(self, reason):
        self.__getitem__(OutDial.__cmd)['reason'] = reason
        return self
