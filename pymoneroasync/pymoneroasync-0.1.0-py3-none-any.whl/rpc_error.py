from sansio_jsonrpc import JsonRpcApplicationError


class WrongParamError(JsonRpcApplicationError):
    ERROR_CODE = -1
    ERROR_MESSAGE = "Invalid parameter"


class TooBigHeightError(JsonRpcApplicationError):
    ERROR_CODE = -2
    ERROR_MESSAGE = "Height is too large"


class TooBigReserveSizeError(JsonRpcApplicationError):
    ERROR_CODE = -3
    ERROR_MESSAGE = "Reserve size is too large"


class WrongWalletAddressError(JsonRpcApplicationError):
    ERROR_CODE = -4
    ERROR_MESSAGE = "Wrong wallet address"


class InternalError(JsonRpcApplicationError):
    ERROR_CODE = -5
    ERROR_MESSAGE = "Internal Error"


class WrongBlockBlobError(JsonRpcApplicationError):
    ERROR_CODE = -6
    ERROR_MESSAGE = "Wrong block blob"


class BlockNotAcceptedError(JsonRpcApplicationError):
    ERROR_CODE = -7
    ERROR_MESSAGE = "Block not accepted"


class CoreBusyError(JsonRpcApplicationError):
    ERROR_CODE = -9
    ERROR_MESSAGE = "Core is busy"


class WrongBlockBlobSizeError(JsonRpcApplicationError):
    ERROR_CODE = -10
    ERROR_MESSAGE = "Wrong block blob size"


class UnsupportedRpcError(JsonRpcApplicationError):
    ERROR_CODE = -11
    ERROR_MESSAGE = "Unsupported RPC"


class MiningToSubAddressError(JsonRpcApplicationError):
    ERROR_CODE = -12
    ERROR_MESSAGE = "Mining to subaddress is not supported"


class RegtestRequiredError(JsonRpcApplicationError):
    ERROR_CODE = -13
    ERROR_MESSAGE = "Regtest mode required"


class PaymentRequiredError(JsonRpcApplicationError):
    ERROR_CODE = -14
    ERROR_MESSAGE = "Payment required"


class InvalidClientError(JsonRpcApplicationError):
    ERROR_CODE = -15
    ERROR_MESSAGE = "Invalid client"


class PaymentTooLowError(JsonRpcApplicationError):
    ERROR_CODE = -16
    ERROR_MESSAGE = "Payment too low"


class DuplicatePaymentError(JsonRpcApplicationError):
    ERROR_CODE = -17
    ERROR_MESSAGE = "Duplicate payment"


class StalePaymentError(JsonRpcApplicationError):
    ERROR_CODE = -18
    ERROR_MESSAGE = "Stale payment"


class CodeRestrictedError(JsonRpcApplicationError):
    ERROR_CODE = -19
    ERROR_MESSAGE = "Parameters beyond restricted allowance"
