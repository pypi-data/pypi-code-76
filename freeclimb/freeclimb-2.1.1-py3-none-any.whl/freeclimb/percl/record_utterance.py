class RecordUtterance(dict):

    __cmd = 'RecordUtterance'

    def __init__(self, action_url):
        super().__init__()
        self.__setitem__(RecordUtterance.__cmd, {})
        self.action_url(action_url)

    def action_url(self, action_url):
        self.__getitem__(RecordUtterance.__cmd)['actionUrl'] = action_url
        return self

    def silence_timeout_ms(self, silence_timeout_ms):
        self.__getitem__(RecordUtterance.__cmd)['silenceTimeoutMs'] = silence_timeout_ms
        return self

    def play_beep(self, play_beep):
        self.__getitem__(RecordUtterance.__cmd)['playBeep'] = play_beep
        return self

    def max_length_sec(self, max_length_sec):
        self.__getitem__(RecordUtterance.__cmd)['maxLengthSec'] = max_length_sec
        return self

    def auto_start(self, auto_start):
        self.__getitem__(RecordUtterance.__cmd)['autoStart'] = auto_start
        return self

    def finish_on_key(self, finish_on_key):
        self.__getitem__(RecordUtterance.__cmd)['finishOnKey'] = finish_on_key
        return self
