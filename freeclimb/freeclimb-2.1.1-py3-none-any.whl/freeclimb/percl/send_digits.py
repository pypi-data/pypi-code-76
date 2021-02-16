class SendDigits(dict):

    __cmd = 'SendDigits'

    def __init__(self, digits):
        super().__init__()
        self.__setitem__(SendDigits.__cmd, {})
        self.digits(digits)

    def digits(self, digits):
        self.__getitem__(SendDigits.__cmd)['digits'] = digits
        return self

    def pause_ms(self, pause_ms):
        self.__getitem__(SendDigits.__cmd)['pauseMs'] = pause_ms
        return self
