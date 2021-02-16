class Play(dict):

    __cmd = 'Play'

    def __init__(self, file):
        super().__init__()
        self.__setitem__(Play.__cmd, {})
        self.file(file)

    def file(self, file):
        self.__getitem__(Play.__cmd)['file'] = file
        return self

    def loop(self, loop):
        self.__getitem__(Play.__cmd)['loop'] = loop
        return self

    def conference_id(self, conference_id):
        self.__getitem__(Play.__cmd)['conferenceId'] = conference_id
        return self
