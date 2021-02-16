class StartRecordCall(dict):

    __cmd = 'StartRecordCall'

    def __init__(self):
        super().__init__()
        self.__setitem__(StartRecordCall.__cmd, {})
