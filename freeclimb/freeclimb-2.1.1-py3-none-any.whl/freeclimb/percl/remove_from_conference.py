class RemoveFromConference(dict):

    __cmd = 'RemoveFromConference'

    def __init__(self, call_id):
        super().__init__()
        self.__setitem__(RemoveFromConference.__cmd, {})
        self.call_id(call_id)

    def call_id(self, call_id):
        self.__getitem__(RemoveFromConference.__cmd)['callId'] = call_id
        return self
