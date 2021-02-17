class ModbusTcpError(Exception):
    """Base class"""


class InvalidFrame(ModbusTcpError):
    """Frame was invalid"""
