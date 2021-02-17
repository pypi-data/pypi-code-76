class ModbusTcpError(Exception):
    """Base class"""


class InvalidFrame(ModbusTcpError):
    """Frame was invalid"""


class IllegalAddress(ModbusTcpError):
    """The address was illegal"""


class IllegalValue(ModbusTcpError):
    """The value was illegal"""


class GatewayTargetDeviceFailedToRespond(ModbusTcpError):
    """Gateway target device failed to respond"""


class GatewayPathUnavailable(ModbusTcpError):
    """Gateway path unavailable"""
