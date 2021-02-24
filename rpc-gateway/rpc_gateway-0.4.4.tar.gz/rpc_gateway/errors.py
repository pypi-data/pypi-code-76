class HardwareGatewayError(Exception):
    pass


class InstanceNotFoundError(HardwareGatewayError):
    pass


class InstanceLockedError(HardwareGatewayError):
    pass


class InvalidInstanceError(HardwareGatewayError):
    pass


class GroupNotFoundError(HardwareGatewayError):
    pass


class InvalidMethodError(HardwareGatewayError):
    pass


class InstanceAlreadyRegisteredError(HardwareGatewayError):
    pass


class InstanceReadOnly(HardwareGatewayError):
    pass


class InvalidMessageError(HardwareGatewayError):
    pass


class InvalidRequestError(HardwareGatewayError):
    pass


class InvalidResponseError(HardwareGatewayError):
    pass


class InvalidPathError(HardwareGatewayError):
    pass


class NotConnectedError(HardwareGatewayError):
    pass


class InvalidMessageIdError(HardwareGatewayError):
    pass


class RequestTimeoutError(HardwareGatewayError):
    pass


class ConnectionError(HardwareGatewayError):
    pass


class ServerConnectionLostError(HardwareGatewayError):
    pass


class SerializationError(HardwareGatewayError):
    pass
