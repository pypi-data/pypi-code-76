class Output:
    """Collect output from microcontroller"""

    def __init__(self, kernel):
        self.__kernel = kernel

    def __convert(self, value):
        if not value or self.__kernel.silent: return ""
        if isinstance(value, bytes):
            try:
                value = value.decode()
            except UnicodeDecodeError:
                pass
        value = str(value)
        # Remove '\r' - output on mac at least comes garbled otherwise
        # Probably because \r\n don't always arrive from micropython in same bytes object
        value = value.replace('\r', '')
        value = value.replace('\x04', '')
        return value if value else ""

    def ans(self, value):
        self.__kernel.print(self.__convert(value))

    def err(self, value):
        self.__kernel.error(self.__convert(value))
