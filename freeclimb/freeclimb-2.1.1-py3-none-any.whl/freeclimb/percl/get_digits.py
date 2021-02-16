class GetDigits(dict):

    __cmd = 'GetDigits'

    def __init__(self, action_url):
        super().__init__()
        self.__setitem__(GetDigits.__cmd, {})
        self.action_url(action_url)

    def action_url(self, action_url):
        self.__getitem__(GetDigits.__cmd)['actionUrl'] = action_url
        return self

    def initial_timeout_ms(self, initial_timeout_ms):
        self.__getitem__(GetDigits.__cmd)['initialTimeoutMs'] = initial_timeout_ms
        return self

    def digit_timeout_ms(self, digit_timeout_ms):
        self.__getitem__(GetDigits.__cmd)['digitTimeoutMs'] = digit_timeout_ms
        return self

    def finish_on_key(self, finish_on_key):
        self.__getitem__(GetDigits.__cmd)['finishOnKey'] = finish_on_key
        return self

    def min_digits(self, min_digits):
        self.__getitem__(GetDigits.__cmd)['minDigits'] = min_digits
        return self

    def max_digits(self, max_digits):
        self.__getitem__(GetDigits.__cmd)['maxDigits'] = max_digits
        return self

    def flush_buffer(self, flush_buffer):
        self.__getitem__(GetDigits.__cmd)['flushBuffer'] = flush_buffer
        return self

    def prompts(self, prompt):
        if 'prompts' not in self.__getitem__(GetDigits.__cmd):
            self.__getitem__(GetDigits.__cmd)['prompts'] = []
        self.__getitem__(GetDigits.__cmd)['prompts'].append(prompt)
        return self

    def enforcePCI(self, enforcePCI):
        self.__getitem__(GetDigits.__cmd)['enforcePCI'] = enforcePCI
        return self
