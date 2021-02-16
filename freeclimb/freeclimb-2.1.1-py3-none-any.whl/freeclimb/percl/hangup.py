class Hangup(dict):

    __cmd = 'Hangup'

    def __init__(self):
        super().__init__()
        self.__setitem__(Hangup.__cmd, {})

    def call_id(self, call_id):
        self.__getitem__(Hangup.__cmd)['callId'] = call_id
        return self

    def reason(self, reason):
        self.__getitem__(Hangup.__cmd)['reason'] = reason
        return self
