class SetListen(dict):

    __cmd = 'SetListen'

    def __init__(self, call_id):
        super().__init__()
        self.__setitem__(SetListen.__cmd, {})
        self.call_id(call_id)

    def call_id(self, call_id):
        self.__getitem__(SetListen.__cmd)['callId'] = call_id
        return self

    def listen(self, listen):
        self.__getitem__(SetListen.__cmd)['listen'] = listen
        return self
