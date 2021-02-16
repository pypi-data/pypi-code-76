class AddressValueError(ValueError):
    def __init__(self, address, message='bad ipv4 address value'):
        self._address = address
        self._message = message
        super().__init__(self._message)
    def __str__(self):
        return f'{self._message} : {self._address}'

class NetworkValueError(ValueError):
    def __init__(self, network, message='bad ipv4 network value'):
        self._network = network
        self._message = message
        super().__init__(self._message)
    def __str__(self):
        return f'{self._message} : {self._network}'
