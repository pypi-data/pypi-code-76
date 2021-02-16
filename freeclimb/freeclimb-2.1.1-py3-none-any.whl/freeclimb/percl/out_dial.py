class OutDial(dict):

    __cmd = 'OutDial'

    def __init__(self, destination, calling_number, action_url, call_connect_url):
        super().__init__()
        self.__setitem__(OutDial.__cmd, {})
        self.destination(destination)
        self.calling_number(calling_number)
        self.action_url(action_url)
        self.call_connect_url(call_connect_url)

    def action_url(self, action_url):
        self.__getitem__(OutDial.__cmd)['actionUrl'] = action_url
        return self

    def call_connect_url(self, call_connect_url):
        self.__getitem__(OutDial.__cmd)['callConnectUrl'] = call_connect_url
        return self

    def calling_number(self, calling_number):
        self.__getitem__(OutDial.__cmd)['callingNumber'] = calling_number
        return self

    def destination(self, destination):
        self.__getitem__(OutDial.__cmd)['destination'] = destination
        return self

    def if_machine(self, if_machine):
        self.__getitem__(OutDial.__cmd)['ifMachine'] = if_machine
        return self

    def if_machine_url(self, if_machine_url):
        self.__getitem__(OutDial.__cmd)['ifMachineUrl'] = if_machine_url
        return self

    def send_digits(self, send_digits):
        self.__getitem__(OutDial.__cmd)['sendDigits'] = send_digits
        return self

    def status_callback_url(self, status_callback_url):
        self.__getitem__(OutDial.__cmd)['statusCallbackUrl'] = status_callback_url
        return self

    def timeout(self, timeout):
        self.__getitem__(OutDial.__cmd)['timeout'] = timeout
        return self
