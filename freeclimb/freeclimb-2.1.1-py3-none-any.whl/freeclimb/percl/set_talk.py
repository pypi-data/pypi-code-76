class SetTalk(dict):

    __cmd = 'SetTalk'

    def __init__(self, call_id):
        super().__init__()
        self.__setitem__(SetTalk.__cmd, {})
        self.call_id(call_id)

    def call_id(self, call_id):
        self.__getitem__(SetTalk.__cmd)['callId'] = call_id
        return self

    def talk(self, talk):
        self.__getitem__(SetTalk.__cmd)['talk'] = talk
        return self
