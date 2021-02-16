class Sms(dict):

    __cmd = 'Sms'

    def __init__(self, to_number, from_number, text):
        super().__init__()
        self.__setitem__(Sms.__cmd, {})
        self.to_number(to_number)
        self.from_number(from_number)
        self.text(text)

    def to_number(self, to_number):
        self.__getitem__(Sms.__cmd)['to'] = to_number
        return self

    def from_number(self, from_number):
        self.__getitem__(Sms.__cmd)['from'] = from_number
        return self

    def text(self, text):
        self.__getitem__(Sms.__cmd)['text'] = text
        return self

    def notification_url(self, notificationUrl):
        self.__getitem__(Sms.__cmd)['notificationUrl'] = notificationUrl
        return self
