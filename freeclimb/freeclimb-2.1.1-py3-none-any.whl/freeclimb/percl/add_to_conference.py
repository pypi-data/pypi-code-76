class AddToConference(dict):

    __cmd = 'AddToConference'

    def __init__(self, conference_id, call_id):
        super().__init__()
        self.__setitem__(AddToConference.__cmd, {})
        self.conference_id(conference_id)
        self.call_id(call_id)

    def conference_id(self, conference_id):
        self.__getitem__(AddToConference.__cmd)['conferenceId'] = conference_id
        return self

    def call_id(self, call_id):
        self.__getitem__(AddToConference.__cmd)['callId'] = call_id
        return self

    def start_conf_on_enter(self, start_conf_on_enter):
        self.__getitem__(AddToConference.__cmd)['startConfOnEnter'] = start_conf_on_enter
        return self

    def talk(self, talk):
        self.__getitem__(AddToConference.__cmd)['talk'] = talk
        return self

    def listen(self, listen):
        self.__getitem__(AddToConference.__cmd)['listen'] = listen
        return self

    def allow_call_control(self, allow_call_control):
        self.__getitem__(AddToConference.__cmd)['allowCallControl'] = allow_call_control
        return self

    def call_control_sequence(self, call_control_sequence):
        self.__getitem__(AddToConference.__cmd)['callControlSequence'] = call_control_sequence
        return self

    def call_control_url(self, call_control_url):
        self.__getitem__(AddToConference.__cmd)['callControlUrl'] = call_control_url
        return self

    def leave_conference_url(self, leave_conference_url):
        self.__getitem__(AddToConference.__cmd)['leaveConferenceUrl'] = leave_conference_url
        return self

    def notification_url(self, notification_url):
        self.__getitem__(AddToConference.__cmd)['notificationUrl'] = notification_url
        return self
