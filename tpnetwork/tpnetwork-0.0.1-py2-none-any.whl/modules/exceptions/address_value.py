class AddressValueError(ValueError):
    def __init__(self, address, message='Bad IP Address format'):
        self._address = address
        self._message = message
        super().__init__(self._message)
    
    def __str__(self):
        return f'{self._message} : {self._address}'
