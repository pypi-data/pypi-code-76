class CustomError(Exception):
    pass


class DataError(CustomError):
    pass


class FTPConnectionError(CustomError):
    pass


class FTPDownloadError(CustomError):
    pass


class FTPUploadError(CustomError):
    pass


class FTPEncodingError(CustomError):
    pass


class RedashAPIError(CustomError):
    pass
