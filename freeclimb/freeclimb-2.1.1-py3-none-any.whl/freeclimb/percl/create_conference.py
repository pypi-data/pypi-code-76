class CreateConferencePlayBeep:
    always = 'always'
    never = 'never'
    entryOnly = 'entryOnly'
    exitOnly = 'exitOnly'


class CreateConference(dict):

    __cmd = 'CreateConference'

    def __init__(self, action_url):
        super().__init__()
        self.__setitem__(CreateConference.__cmd, {})
        self.action_url(action_url)

    def action_url(self, action_url):
        self.__getitem__(CreateConference.__cmd)['actionUrl'] = action_url
        return self

    def alias(self, alias):
        self.__getitem__(CreateConference.__cmd)['alias'] = alias
        return self

    def play_beep(self, play_beep):
        self.__getitem__(CreateConference.__cmd)['playBeep'] = play_beep
        return self

    def record(self, record):
        self.__getitem__(CreateConference.__cmd)['record'] = record
        return self

    def wait_url(self, wait_url):
        self.__getitem__(CreateConference.__cmd)['waitUrl'] = wait_url
        return self

    def status_callback_url(self, status_callback_url):
        self.__getitem__(CreateConference.__cmd)['statusCallbackUrl'] = status_callback_url
        return self
