#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#


class OnBoardingError(Exception):
    pass

class UserCredentialsError(OnBoardingError):
    pass


class DeviceRegisterError(OnBoardingError):
    pass


class DeviceDeregisterError(OnBoardingError):
    pass


class DeviceConfigureError(OnBoardingError):
    pass


class ConfigValidationError(OnBoardingError):
    pass


class GenerateKeysError(OnBoardingError):
    pass


class BoardError(OnBoardingError):
    pass


class ConnectorError(OnBoardingError):
    pass


class ConnectorExecuteError(ConnectorError):
    pass


class CloudAccessError(OnBoardingError):
    pass
