class TerminateConference(dict):

    __cmd = 'TerminateConference'

    def __init__(self, conference_id):
        super().__init__()
        self.__setitem__(TerminateConference.__cmd, {})
        self.conference_id(conference_id)

    def conference_id(self, conference_id):
        self.__getitem__(TerminateConference.__cmd)['conferenceId'] = conference_id
        return self
